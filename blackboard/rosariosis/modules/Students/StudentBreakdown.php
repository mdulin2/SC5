<?php

require_once 'ProgramFunctions/Charts.fnc.php';

DrawHeader( ProgramTitle() );

$_REQUEST['field_id'] = issetVal( $_REQUEST['field_id'] );

$chart_types = [ 'bar', 'pie', 'list' ];

// set Chart Type
if ( ! isset( $_REQUEST['chart_type'] )
	|| ! in_array( $_REQUEST['chart_type'], $chart_types ) )
{
	$_REQUEST['chart_type'] = 'bar';
}

$chartline = false;

// Advanced Search
if ( $_REQUEST['modfunc'] === 'search' )
{
	echo '<br />';

	$extra['new'] = true;

	$extra['search_title'] = _( 'Advanced' );

	$extra['action'] = '&field_id=' . $_REQUEST['field_id'] .
		'&chart_type=' . $_REQUEST['chart_type'] .
		'&modfunc=&search_modfunc=';

	Search( 'student_id', $extra );
}

if ( ! empty( $_REQUEST['field_id'] ) )
{
	if ( $_REQUEST['field_id'] === 'grade_level' )
	{
		// @since 7.1 Add Grade Level breakdown.
		$fields_RET[1]['TITLE'] = _( 'Grade Level' );

		$fields_RET[1]['TYPE'] = 'select';

		$fields_RET[1]['OPTIONS'] = [];

		$grade_levels_RET = DBGet( "SELECT TITLE
			FROM school_gradelevels
			WHERE SCHOOL_ID='" . UserSchool() . "'
			ORDER BY SORT_ORDER IS NULL,SORT_ORDER" );

		foreach ( (array) $grade_levels_RET as $grade_level )
		{
			$fields_RET[1]['OPTIONS'][] = $grade_level['TITLE'];
		}

		$field_column = 'ssm.GRADE_ID';
	}
	else
	{
		$fields_RET = DBGet( "SELECT TITLE,SELECT_OPTIONS AS OPTIONS,TYPE
			FROM custom_fields WHERE ID='" . (int) $_REQUEST['field_id'] . "'" );

		if ( $fields_RET[1]['OPTIONS'] )
		{
			$fields_RET[1]['OPTIONS'] = explode( "\r", str_replace( [ "\r\n", "\n" ], "\r", $fields_RET[1]['OPTIONS'] ) );
		}

		$field_column = 's.CUSTOM_' . intval( $_REQUEST['field_id'] );
	}

	$extra = [];

	if ( in_array( $fields_RET[1]['TYPE'], [ 'select', 'autos', 'exports' ] ) )
	{
		// Autos pull-down fields.
		if ( $fields_RET[1]['TYPE'] === 'autos' )
		{
			// Add values found in current year.
			$options_RET = DBGet( "SELECT DISTINCT " . $field_column . ",upper(" . $field_column . ") AS SORT_KEY
				FROM students s,student_enrollment sse
				WHERE sse.STUDENT_ID=s.STUDENT_ID
				AND (sse.SYEAR='" . UserSyear() . "')
				AND s.CUSTOM_" . intval( $_REQUEST['field_id'] ) . " IS NOT NULL
				AND s.CUSTOM_" . intval( $_REQUEST['field_id'] ) . " != ''
				ORDER BY SORT_KEY" );

			foreach ( (array) $options_RET as $option )
			{
				if ( ! $fields_RET[1]['OPTIONS']
					|| ! in_array( $option['CUSTOM_' . intval( $_REQUEST['field_id'] )], $fields_RET[1]['OPTIONS'] ) )
				{
					$fields_RET[1]['OPTIONS'][] = $option['CUSTOM_' . intval( $_REQUEST['field_id'] )];
				}
			}
		}

		$extra['SELECT_ONLY'] = "COUNT(*) AS COUNT ";

		if ( $_REQUEST['field_id'] === 'grade_level' )
		{
			$extra['SELECT_ONLY'] .= ",COALESCE((SELECT TITLE
				FROM school_gradelevels
				WHERE ID=" . $field_column . "),'*BLANK*') AS TITLE ";
		}
		else
		{
			$extra['SELECT_ONLY'] .= ",COALESCE(" . $field_column . ",'*BLANK*') AS TITLE ";
		}

		$extra['GROUP'] = $field_column;

		$extra['group'] = [ 'TITLE' ];

		$totals_RET = GetStuList( $extra );

		$chart['chart_data'][0][] = _( 'No Value' );

		$chart['chart_data'][1][] = (int) issetVal( $totals_RET['*BLANK*'][1]['COUNT'] );

		foreach ( (array) $fields_RET[1]['OPTIONS'] as $option )
		{
			$chart['chart_data'][0][] = $option;

			$chart['chart_data'][1][] = (int) issetVal( $totals_RET[ $option ][1]['COUNT'] );
		}
	}
	elseif ( $fields_RET[1]['TYPE'] === 'multiple' )
	{
		$extra['SELECT_ONLY'] = $field_column . " AS TITLE ";

		$student_RET = GetStuList( $extra );

		foreach ( (array) $student_RET as $student )
		{
			$student['TITLE'] = explode( "||", trim( $student['TITLE'], '|' ) );

			foreach ( (array) $student['TITLE'] as $option )
			{
				if ( ! isset( $options_count[ $option ] ) )
				{
					$options_count[ $option ] = 0;
				}

				$options_count[ $option ]++;
			}
		}

		foreach ( (array) $fields_RET[1]['OPTIONS'] as $option )
		{
			$chart['chart_data'][0][] = $option;

			$chart['chart_data'][1][] = issetVal( $options_count[ $option ], 0 );
		}
	}
	elseif ( $fields_RET[1]['TYPE'] === 'radio' )
	{
		$extra['SELECT_ONLY'] = "COALESCE(" . $field_column . ",'N') AS TITLE,COUNT(*) AS COUNT ";

		$extra['GROUP'] = $field_column;

		$extra['group'] = [ 'TITLE' ];

		$totals_RET = GetStuList( $extra );

		$chart['chart_data'][0][] = _( 'Yes' );

		$chart['chart_data'][1][] = (int) issetVal( $totals_RET['Y'][1]['COUNT'] );

		$chart['chart_data'][0][] = _( 'No' );

		$chart['chart_data'][1][] = (int) issetVal( $totals_RET['N'][1]['COUNT'] );
	}
	elseif ( $fields_RET[1]['TYPE'] === 'numeric' )
	{
		$extra['SELECT_ONLY'] = "COALESCE(max(" . $field_column . "),0) as MAX,COALESCE(min(" . $field_column . "),0) AS MIN ";

		// Remove NULL entries.
		$extra['WHERE'] = "AND " . $field_column . " IS NOT NULL ";

		$max_min_RET = GetStuList( $extra );

		$diff = $max_min_RET[1]['MAX'] - $max_min_RET[1]['MIN'];

		if ( $diff > 10
			&& $_REQUEST['chart_type'] !== 'bar' )
		{
			// Correct numeric chart.
			for ( $i = 1; $i <= 10; $i++ )
			{
				/*$chart['chart_data'][0][ $i ] = (ceil($diff/5)*($i-1)).' - '.((ceil($diff/5)*$i)-1);
				$mins[ $i ] = (ceil($diff/5)*($i-1));
				$chart['chart_data'][1][ $i ] = 0;*/

				$chart['chart_data'][0][ $i ] = ( $max_min_RET[1]['MIN'] + ( ceil( $diff / 10 ) * ( $i - 1 ) ) ) . ' - ' .
					( $max_min_RET[1]['MIN'] + ( ( ceil( $diff / 10 ) * $i ) - 1 ) );

				$mins[ $i ] = ( $max_min_RET[1]['MIN'] + ( ceil( $diff / 10 ) * ( $i - 1 ) ) );

				$chart['chart_data'][1][ $i ] = 0;
			}

			//$chart['chart_data'][0][$i-1] = ($max_min_RET[1]['MIN'] + (ceil($diff/5)*($i-2))).'+';
			$mins[ $i ] = ( ceil( $diff / 10 ) * ( $i - 1 ) );
		}
		else // Transform column chart in line chart.
		{
			$chartline = true;
		}

		$extra['SELECT_ONLY'] = $field_column . " AS TITLE";

		$extra['functions'] = [ 'TITLE' => 'makeNumeric' ];

		$students_RET = GetStuList( $extra );

		if ( ! $students_RET ) // Bugfix no results for numeric fields chart.
		{
			$chart['chart_data'][0][0] = $chart['chart_data'][1][0] = 0;
		}
	}
}

if ( ! $_REQUEST['modfunc'] )
{
	echo '<form action="' . PreparePHP_SELF( $_REQUEST ) . '" method="GET">';

	$fields_RET = DBGet( "SELECT ID,TITLE,SELECT_OPTIONS AS OPTIONS,CATEGORY_ID
		FROM custom_fields
		WHERE TYPE NOT IN ('textarea','text','date','log','holder','files')
		ORDER BY SORT_ORDER IS NULL,SORT_ORDER,TITLE", [], [ 'CATEGORY_ID' ] );

	$categories_RET = DBGet( "SELECT ID,TITLE
		FROM student_field_categories", [], [ 'ID' ] );

	$select = '<select name="field_id" onchange="ajaxPostForm(this.form,true);">';

	$select .= '<option value="">' . _( 'Please choose a student field' ) . '</option>';

	$selected = '';

	if ( $_REQUEST['field_id'] === 'grade_level' )
	{
		$selected = ' selected';
		$field_title = _( 'Grade Level' );
	}

	// @since 7.1 Add Grade Level breakdown.
	$select .= '<option value="grade_level"' . $selected . '>' . _( 'Grade Level' ) . '</option>';

	foreach ( (array) $fields_RET as $field_id => $fields )
	{
		$select .= '<optgroup label="' . ParseMLField( $categories_RET[ $field_id ][1]['TITLE'] ) . '">';

		foreach ( (array) $fields as $field )
		{
			$selected = '';

			if ( $_REQUEST['field_id'] == $field['ID'] )
			{
				$selected = ' selected';
				$field_title = $field['TITLE'];
			}

			$select .= '<option value="' . AttrEscape( $field['ID'] ) . '"' . $selected . '>' . ParseMLField( $field['TITLE'] ) . '</option>';
		}

		$select .= '</optgroup>';
	}

	$select .= '</select>';

	$advanced_link = ' <a href="' . PreparePHP_SELF( $_REQUEST, [ 'search_modfunc' ], [
		'modfunc' => 'search',
		'include_top' => 'false',
	] ) . '">' . _( 'Advanced' ) . '</a>';

	DrawHeader( $select . $advanced_link );

	if ( ! empty( $_ROSARIO['SearchTerms'] ) )
	{
		DrawHeader( $_ROSARIO['SearchTerms'] );
	}

	echo '<br />';

	if ( isset( $_REQUEST['field_id'] )
		&& !empty( $_REQUEST['field_id'] ) )
	{
		if ( $chartline )
		{
			// Force Chart Type to bar if Line
			if ( $_REQUEST['chart_type'] === 'pie' )
			{
				$_REQUEST['chart_type'] = 'bar';
			}

			$tabs = [
				[
					'title' => _( 'Line' ),
					'link' => PreparePHP_SELF( $_REQUEST, [], [ 'chart_type' => 'bar' ] ),
				],
				[
					'title' => _( 'List' ),
					'link' => PreparePHP_SELF( $_REQUEST, [], [ 'chart_type' => 'list' ] ),
				]
			];
		}
		else
		{
			$tabs = [
				[
					'title' => _( 'Column' ),
					'link' => PreparePHP_SELF( $_REQUEST, [], [ 'chart_type' => 'bar' ] ),
				],
				[
					'title' => _( 'Pie' ),
					'link' => PreparePHP_SELF( $_REQUEST, [], [ 'chart_type' => 'pie' ] ),
				],
				[
					'title' => _( 'List' ),
					'link' => PreparePHP_SELF( $_REQUEST, [], [ 'chart_type' => 'list' ] ),
				]
			];
		}

		$_ROSARIO['selected_tab'] = PreparePHP_SELF( $_REQUEST );

		PopTable( 'header', $tabs );

		if ( $_REQUEST['chart_type'] === 'list' )
		{
			$chart_data = [ '0' => '' ];

			foreach ( (array) $chart['chart_data'][1] as $key => $value )
			{
				$chart_data[] = [ 'TITLE' => $chart['chart_data'][0][ $key ], 'VALUE' => $value ];
			}

			unset( $chart_data[0] );

			$LO_options['responsive'] = false;

			$LO_columns = [ 'TITLE' => _( 'Option' ), 'VALUE' => _( 'Number of Students' ) ];

			ListOutput( $chart_data, $LO_columns, 'Option', 'Options', [], [], $LO_options );
		}
		// Chart.js charts.
		else
		{
			$search_terms = '';

			if ( ! empty( $_ROSARIO['SearchTerms'] ) )
			{
				$search_terms = ' - ' . strip_tags( str_replace( '<br />', " - ", mb_substr( $_ROSARIO['SearchTerms'], 0, -6 ) ));
			}

			$chart_title = sprintf( _( '%s Breakdown' ), ParseMLField( $field_title ) ) . $search_terms;

			if ( $_REQUEST['chart_type'] === 'pie' )
			{
				foreach ( (array) $chart['chart_data'][0] as $index => $label )
				{
					if ( ! is_numeric( $chart['chart_data'][1][ $index ] ) )
					{
						continue;
					}

					// Limit label to 30 char max.
					$chart['chart_data'][0][ $index ] = mb_substr( $label, 0, 30 );
				}
			}

			echo ChartjsChart(
				$chartline ? 'line' : $_REQUEST['chart_type'],
				$chart['chart_data'],
				$chart_title
			);
		}

		PopTable( 'footer' );
	}

	echo '</form>';
}
