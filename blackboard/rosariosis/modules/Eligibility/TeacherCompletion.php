<?php
require_once 'ProgramFunctions/TipMessage.fnc.php';

$_REQUEST['period'] = (int) issetVal( $_REQUEST['period'] );

DrawHeader( ProgramTitle() );

// GET ALL THE CONFIG ITEMS FOR ELIGIBILITY
$eligibility_config = ProgramConfig( 'eligibility' );

foreach ( (array) $eligibility_config as $value )
{
	${$value[1]['TITLE']} = $value[1]['VALUE'];
}

// Day of the week: 1 (for Monday) through 7 (for Sunday).
$today = date( 'w' ) ? date( 'w' ) : 7;

$start = time() - ( $today - $START_DAY ) * 60 * 60 * 24;

if ( empty( $_REQUEST['start_date'] ) )
{
	$start_time = $start;

	$start_date = date( 'Y-m-d', $start_time );

	$end_date = date( 'Y-m-d' );
}
else
{
	$start_time = (int) $_REQUEST['start_date'];

	$start_date = date( 'Y-m-d', $start_time );

	$end_date = date( 'Y-m-d', $start_time + 60 * 60 * 24 * 7 );
}

$periods_RET = DBGet( "SELECT sp.PERIOD_ID,sp.TITLE,COALESCE(sp.SHORT_NAME,sp.TITLE) AS SHORT_TITLE
	FROM school_periods sp
	WHERE sp.SCHOOL_ID='" . UserSchool() . "'
	AND sp.SYEAR='" . UserSyear() . "'
	AND EXISTS (SELECT 1
		FROM course_periods cp,course_period_school_periods cpsp
		WHERE cpsp.PERIOD_ID=sp.PERIOD_ID
		AND cpsp.COURSE_PERIOD_ID=cp.COURSE_PERIOD_ID
		AND cp.SCHOOL_ID='" . UserSchool() . "'
		AND cp.SYEAR='" . UserSyear() . "')
	ORDER BY sp.SORT_ORDER IS NULL,sp.SORT_ORDER,sp.TITLE" );

$period_select = '<select name="period" id="period"><option value="">' . _( 'All' ) . '</option>';

foreach ( (array) $periods_RET as $period )
{
	$period_select .= '<option value="' . AttrEscape( $period['PERIOD_ID'] ) . '"' .
		( $_REQUEST['period'] == $period['PERIOD_ID'] ? ' selected' : '' ) . '>' .
		$period['TITLE'] . '</option>';
}

$period_select .= '</select>';

echo '<form action="' . URLEscape( 'Modules.php?modname=' . $_REQUEST['modname']  ) . '" method="GET">';

$begin_year = DBGetOne( "SELECT min(" . _SQLUnixTimestamp( 'SCHOOL_DATE' ) . ") AS SCHOOL_DATE
	FROM attendance_calendar
	WHERE SCHOOL_ID='" . UserSchool() . "'
	AND SYEAR='" . UserSyear() . "'" );

if ( $start
	&& $begin_year )
{
	$date_select = '<option value="' . AttrEscape( $start ) . '">' .
	ProperDate( date( 'Y-m-d', $start ) ) . ' - ' . ProperDate( DBDate() ) . '</option>';

	for ( $i = $start - ( 60 * 60 * 24 * 7 ); $i >= $begin_year; $i -= ( 60 * 60 * 24 * 7 ) )
	{
		$date_select .= '<option value="' . AttrEscape( $i ) . '"' .
		(  ( $i + 86400 >= $start_time && $i - 86400 <= $start_time ) ? ' selected' : '' ) . '>' .
		ProperDate( date( 'Y-m-d', $i ) ) . ' - ' .
		ProperDate( date( 'Y-m-d', ( $i + 1 + (  ( $END_DAY - $START_DAY ) ) * 60 * 60 * 24 ) ) ) . '</option>';
	}
}

$date_select = '<select name="start_date" id="start_date">' . $date_select . '</select>';

DrawHeader( '<label for="start_date">' . _( 'Timeframe' ) . ':</label> ' . $date_select . ' &mdash; ' .
	'<label for="period">' . _( 'Period' ) . ':</label> ' . $period_select . ' ' .
	SubmitButton( _( 'Go' ) ) );

echo '</form>';

//FJ multiple school periods for a course period
/*$sql = "SELECT " . DisplayNameSQL( 's' ) . " AS FULL_NAME,sp.TITLE,cp.PERIOD_ID,s.STAFF_ID
FROM staff s,course_periods cp,school_periods sp
WHERE
sp.PERIOD_ID = cp.PERIOD_ID
AND cp.TEACHER_ID=s.STAFF_ID AND cp.MARKING_PERIOD_ID IN (".GetAllMP('QTR',UserMP()).")
AND cp.SYEAR='".UserSyear()."' AND cp.SCHOOL_ID='".UserSchool()."' AND s.PROFILE='teacher'
".(($_REQUEST['period'])?" AND cp.PERIOD_ID='".$_REQUEST['period']."'":'')."
AND NOT EXISTS (SELECT '' FROM eligibility_completed ac WHERE ac.STAFF_ID=cp.TEACHER_ID AND ac.PERIOD_ID = sp.PERIOD_ID AND ac.SCHOOL_DATE BETWEEN '".$start_date."' AND '".$end_date."')
";*/
$sql = "SELECT " . DisplayNameSQL( 's' ) . " AS FULL_NAME,sp.TITLE,cpsp.PERIOD_ID,
	s.STAFF_ID,s.ROLLOVER_ID,cp.TITLE AS CP_TITLE
	FROM staff s,course_periods cp,school_periods sp,course_period_school_periods cpsp
	WHERE cp.COURSE_PERIOD_ID=cpsp.COURSE_PERIOD_ID
	AND sp.PERIOD_ID=cpsp.PERIOD_ID
	AND cp.TEACHER_ID=s.STAFF_ID
	AND cp.MARKING_PERIOD_ID IN (" . GetAllMP( 'QTR', GetCurrentMP( 'QTR', $start_date ) ) . ")
	AND cp.SYEAR='" . UserSyear() . "'
	AND cp.SCHOOL_ID='" . UserSchool() . "'
	AND s.PROFILE='teacher'" .
	( $_REQUEST['period'] ? " AND cpsp.PERIOD_ID='" . (int) $_REQUEST['period'] . "'" : '' ) .
	"AND NOT EXISTS (SELECT ''
		FROM eligibility_completed ac
		WHERE ac.STAFF_ID=cp.TEACHER_ID
		AND ac.PERIOD_ID=sp.PERIOD_ID
		AND ac.SCHOOL_DATE BETWEEN '" . $start_date . "' AND '" . $end_date . "')";

$RET = DBGet( $sql, [ 'FULL_NAME' => 'makePhotoTipMessage' ], [ 'STAFF_ID', 'PERIOD_ID' ] );

$i = 0;

$staff_RET = [];

foreach ( (array) $RET as $staff_id => $periods )
{
	$i++;

	$staff_RET[$i]['FULL_NAME'] = $periods[key( $periods )][1]['FULL_NAME'];

	if ( empty( $_REQUEST['period'] ) )
	{
		foreach ( (array) $periods as $period_id => $course_periods )
		{
			if ( isset( $_REQUEST['_ROSARIO_PDF'] ) )
			{
				$staff_RET[$i][$period_id] = _( 'No' );

				continue;
			}

			$cp_titles = [];

			foreach ( (array) $course_periods as $course_period )
			{
				$cp_titles[] = $course_period['CP_TITLE'];
			}

			$staff_RET[$i][$period_id] = MakeTipMessage(
				implode( '<br /><br />', $cp_titles ),
				_( 'Course Periods' ),
				button( 'x' )
			);
		}
	}
}

$columns = [ 'FULL_NAME' => _( 'Teacher' ) ];

$period_title_column = 'TITLE';

if ( count( $periods_RET ) > 10 )
{
	// Use Period's Short Name when > 10 columns in the list.
	$period_title_column = 'SHORT_TITLE';
}

if ( empty( $_REQUEST['period'] ) )
{
	foreach ( (array) $periods_RET as $period )
	{
		$columns[$period['PERIOD_ID']] = $period[$period_title_column];
	}
}

ListOutput(
	$staff_RET,
	$columns,
	'Teacher who hasn\'t entered eligibility',
	'Teachers who haven\'t entered eligibility'
);

/**
 * SQL to extract Unix timestamp or epoch from date
 * Use UNIX_TIMESTAMP() for MySQL and extract(EPOCH) for PostgreSQL
 *
 * Local function
 *
 * @since 10.0
 *
 * @param  string $column Date column.
 *
 * @return string         MySQL or PostgreSQL function
 */
function _SQLUnixTimestamp( $column )
{
	global $DatabaseType;

	if ( $DatabaseType === 'mysql' )
	{
		return "UNIX_TIMESTAMP(" . $column . ")";
	}

	return "extract(EPOCH FROM " . $column . ")";
}
