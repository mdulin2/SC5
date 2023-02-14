<?php

DrawHeader( ProgramTitle() );

// Add eventual Dates to $_REQUEST['values'].
AddRequestedDates( 'values', 'post' );

if ( $_REQUEST['modfunc'] === 'update'
	&& ! empty( $_POST['values'] )
	&& AllowEdit() )
{
	foreach ( (array) $_REQUEST['values'] as $id => $columns )
	{
		if ( $id !== 'new' )
		{
			$sql = "UPDATE eligibility_activities SET ";

			foreach ( (array) $columns as $column => $value )
			{
				$sql .= DBEscapeIdentifier( $column ) . "='" . $value . "',";
			}

			$sql = mb_substr( $sql, 0, -1 ) . " WHERE ID='" . (int) $id . "'";
			DBQuery( $sql );
		}

		// New: check for Title
		elseif ( $columns['TITLE'] )
		{
			$sql = "INSERT INTO eligibility_activities ";

			$fields = 'SCHOOL_ID,SYEAR,';
			$values = "'" . UserSchool() . "','" . UserSyear() . "',";

			$go = 0;

			foreach ( (array) $columns as $column => $value )
			{
				if ( ! empty( $value ) || $value == '0' )
				{
					$fields .= DBEscapeIdentifier( $column ) . ',';
					$values .= "'" . $value . "',";
					$go = true;
				}
			}

			$sql .= '(' . mb_substr( $fields, 0, -1 ) . ') values(' . mb_substr( $values, 0, -1 ) . ')';

			if ( $go )
			{
				DBQuery( $sql );
			}
		}
	}

	// Unset modfunc & redirect URL.
	RedirectURL( 'modfunc' );
}

if ( $_REQUEST['modfunc'] === 'remove'
	&& AllowEdit() )
{
	if ( DeletePrompt( _( 'Activity' ) ) )
	{
		DBQuery( "DELETE FROM eligibility_activities
			WHERE ID='" . (int) $_REQUEST['id'] . "'" );

		// Unset modfunc & ID & redirect URL.
		RedirectURL( [ 'modfunc', 'id' ] );
	}
}

if ( ! $_REQUEST['modfunc'] )
{
	$sql = "SELECT ID,TITLE,START_DATE,END_DATE,COMMENT
	FROM eligibility_activities
	WHERE SYEAR='" . UserSyear() . "'
	AND SCHOOL_ID='" . UserSchool() . "'
	ORDER BY TITLE";

	$activities_RET = DBGet(
		DBQuery( $sql ),
		[
			'TITLE' => '_makeTextInput',
			'START_DATE' => '_makeDateInput',
			'END_DATE' => '_makeDateInput',
			'COMMENT' => '_makeTextInput',
		]
	);

	$columns = [
		'TITLE' => _( 'Title' ),
		'START_DATE' => _( 'Begins' ),
		'END_DATE' => _( 'Ends' ),
		'COMMENT' => _( 'Comment' ),
	];

	$link['add']['html'] = [
		'TITLE' => _makeTextInput( '', 'TITLE' ),
		'START_DATE' => _makeDateInput( '', 'START_DATE' ),
		'END_DATE' => _makeDateInput( '', 'END_DATE' ),
		'COMMENT' => _makeTextInput( '', 'COMMENT' ),
	];

	$link['remove']['link'] = 'Modules.php?modname=' . $_REQUEST['modname'] . '&modfunc=remove';

	$link['remove']['variables'] = [ 'id' => 'ID' ];

	echo '<form action="' . URLEscape( 'Modules.php?modname=' . $_REQUEST['modname'] . '&modfunc=update' ) . '" method="POST">';

	DrawHeader( '', SubmitButton() );

	ListOutput( $activities_RET, $columns, 'Activity', 'Activities', $link );

	echo '<div class="center">' . SubmitButton() . '</div></form>';
}

/**
 * @param $value
 * @param $name
 */
function _makeTextInput( $value, $name )
{
	global $THIS_RET;

	$extra = 'maxlength=100';

	if ( ! empty( $THIS_RET['ID'] ) )
	{
		$id = $THIS_RET['ID'];

		if ( $name === 'TITLE' )
		{
			$extra .= ' required';
		}
	}
	else
	{
		$id = 'new';
	}

	if ( $name === 'COMMENT' )
	{
		$extra .= ' size=20';
	}

	return TextInput( $value, 'values[' . $id . '][' . $name . ']', '', $extra );
}

/**
 * @param $value
 * @param $name
 */
function _makeDateInput( $value, $name )
{
	global $THIS_RET;

	if ( ! empty( $THIS_RET['ID'] ) )
	{
		$id = $THIS_RET['ID'];
	}
	else
	{
		$id = 'new';
	}

	return DateInput( $value, 'values[' . $id . '][' . $name . ']', '', true, ( $id === 'new' ) );
}
