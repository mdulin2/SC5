<?php

DrawHeader( ProgramTitle() );

if ( empty( $_REQUEST['table'] ) )
{
	$_REQUEST['table'] = '0';
}

if ( $_REQUEST['modfunc'] === 'update'
	&& AllowEdit() )
{
	if ( ! empty( $_REQUEST['values'] )
		&& ! empty( $_POST['values'] ) )
	{
		foreach ( (array) $_REQUEST['values'] as $id => $columns )
		{
			// FJ fix SQL bug invalid sort order.

			if ( empty( $columns['SORT_ORDER'] ) || is_numeric( $columns['SORT_ORDER'] ) )
			{
				if ( isset( $columns['DEFAULT_CODE'] )
					&& $columns['DEFAULT_CODE'] == 'Y' )
				{
					DBQuery( "UPDATE attendance_codes
						SET DEFAULT_CODE=NULL
						WHERE SYEAR='" . UserSyear() . "'
						AND SCHOOL_ID='" . UserSchool() . "'
						AND TABLE_NAME='" . (int) $_REQUEST['table'] . "'" );
				}

				if ( $id !== 'new' )
				{
					if ( $_REQUEST['table'] !== 'new' )
					{
						$sql = "UPDATE attendance_codes SET ";
					}
					else
					{
						$sql = "UPDATE attendance_code_categories SET ";
					}

					foreach ( (array) $columns as $column => $value )
					{
						$sql .= DBEscapeIdentifier( $column ) . "='" . $value . "',";
					}

					$sql = mb_substr( $sql, 0, -1 ) . " WHERE ID='" . (int) $id . "'";
					DBQuery( $sql );
				}

				// New: check for Title & Short Name.
				elseif ( $columns['TITLE']
					&& ( $_REQUEST['table'] === 'new' || $columns['SHORT_NAME'] ) )
				{
					if ( $_REQUEST['table'] !== 'new' )
					{
						$sql = "INSERT INTO attendance_codes ";
						$fields = 'SCHOOL_ID,SYEAR,TABLE_NAME,';
						$values = "'" . UserSchool() . "','" . UserSyear() . "','" . $_REQUEST['table'] . "',";
					}
					else
					{
						$sql = "INSERT INTO attendance_code_categories ";
						$fields = 'SCHOOL_ID,SYEAR,';
						$values = "'" . UserSchool() . "','" . UserSyear() . "',";
					}

					$go = false;

					foreach ( (array) $columns as $column => $value )
					{
						if ( isset( $value ) && $value != '' )
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
			else
			{
				$error[] = _( 'Please enter a valid Sort Order.' );
			}
		}
	}

	// Unset modfunc & redirect URL.
	RedirectURL( 'modfunc' );
}

if ( $_REQUEST['modfunc'] === 'remove'
	&& AllowEdit() )
{
	if ( $_REQUEST['table'] !== 'new' )
	{
		if ( DeletePrompt( _( 'Attendance Code' ) ) )
		{
			DBQuery( "DELETE FROM attendance_codes WHERE ID='" . (int) $_REQUEST['id'] . "'" );

			// Unset modfunc & ID & redirect URL.
			RedirectURL( [ 'modfunc', 'id' ] );
		}
	}
	elseif ( DeletePrompt( _( 'Category' ) ) )
	{
		$delete_sql = "DELETE FROM attendance_code_categories
			WHERE ID='" . (int) $_REQUEST['id'] . "';";

		$delete_sql .= "DELETE FROM attendance_codes
			WHERE TABLE_NAME='" . (int) $_REQUEST['id'] . "';";

		DBQuery( $delete_sql );

		DBQuery( "UPDATE course_periods
			SET DOES_ATTENDANCE=replace(DOES_ATTENDANCE,'," . (int) $_REQUEST['id'] . ",',',')
			WHERE SYEAR='" . UserSyear() . "'
			AND SCHOOL_ID='" . UserSchool() . "'" );

		DBQuery( "UPDATE course_periods
			SET DOES_ATTENDANCE=NULL
			WHERE DOES_ATTENDANCE=','
			AND SYEAR='" . UserSyear() . "'
			AND SCHOOL_ID='" . UserSchool() . "'" );

		// Unset modfunc & ID & redirect URL.
		RedirectURL( [ 'modfunc', 'id' ] );
	}
}

// FJ fix SQL bug invalid sort order
echo ErrorMessage( $error );

if ( ! $_REQUEST['modfunc'] )
{
	if ( $_REQUEST['table'] !== 'new' )
	{
		$attendance_codes_RET = DBGet( "SELECT ID,TITLE,SHORT_NAME,TYPE,DEFAULT_CODE,STATE_CODE,SORT_ORDER
			FROM attendance_codes
			WHERE SYEAR='" . UserSyear() . "'
			AND SCHOOL_ID='" . UserSchool() . "'
			AND TABLE_NAME='" . (int) $_REQUEST['table'] . "'
			ORDER BY SORT_ORDER IS NULL,SORT_ORDER,TITLE",
			[
				'TITLE' => '_makeTextInput',
				'SHORT_NAME' => '_makeTextInput',
				'SORT_ORDER' => '_makeTextInput',
				'TYPE' => '_makeSelectInput',
				'STATE_CODE' => '_makeSelectInput',
				'DEFAULT_CODE' => '_makeCheckBoxInput',
			]
		);
	}

	$tabs = [ [
		'title' => _( 'Attendance' ),
		'link' => 'Modules.php?modname=' . $_REQUEST['modname'] . '&table=0',
	] ];

	$categories_RET = DBGet( "SELECT ID,TITLE
		FROM attendance_code_categories
		WHERE SYEAR='" . UserSyear() . "'
		AND SCHOOL_ID='" . UserSchool() . "'" );

	foreach ( (array) $categories_RET as $category )
	{
		$tabs[] = [
			'title' => $category['TITLE'],
			'link' => 'Modules.php?modname=' . $_REQUEST['modname'] . '&table=' . $category['ID'],
		];
	}

	if ( $_REQUEST['table'] !== 'new' )
	{
		$sql = "SELECT ID,TITLE,SHORT_NAME,TYPE,DEFAULT_CODE,STATE_CODE,SORT_ORDER
		FROM attendance_codes
		WHERE SYEAR='" . UserSyear() . "'
		AND SCHOOL_ID='" . UserSchool() . "'
		AND TABLE_NAME='" . (int) $_REQUEST['table'] . "'
		ORDER BY SORT_ORDER IS NULL,SORT_ORDER,TITLE";

		$functions = [
			'TITLE' => '_makeTextInput',
			'SHORT_NAME' => '_makeTextInput',
			'SORT_ORDER' => '_makeTextInput',
			'TYPE' => '_makeSelectInput',
			'DEFAULT_CODE' => '_makeCheckBoxInput',
		];

		$LO_columns = [
			'TITLE' => _( 'Title' ),
			'SHORT_NAME' => _( 'Short Name' ),
			'SORT_ORDER' => _( 'Sort Order' ),
			'TYPE' => _( 'Type' ),
			'DEFAULT_CODE' => _( 'Default for Teacher' ),
		];

		if ( $_REQUEST['table'] == '0' )
		{
			$functions['STATE_CODE'] = '_makeSelectInput';
			$LO_columns['STATE_CODE'] = _( 'State Code' );
		}

		$link['add']['html'] = [
			'TITLE' => _makeTextInput( '', 'TITLE' ),
			'SHORT_NAME' => _makeTextInput( '', 'SHORT_NAME' ),
			'SORT_ORDER' => _makeTextInput( '', 'SORT_ORDER' ),
			'TYPE' => _makeSelectInput( '', 'TYPE' ),
			'DEFAULT_CODE' => _makeCheckBoxInput( '', 'DEFAULT_CODE' ),
		];

		if ( $_REQUEST['table'] == '0' )
		{
			$link['add']['html']['STATE_CODE'] = _makeSelectInput( '', 'STATE_CODE' );
		}

		$link['remove']['link'] = 'Modules.php?modname=' . $_REQUEST['modname'] . '&modfunc=remove&table=' . $_REQUEST['table'];
		$link['remove']['variables'] = [ 'id' => 'ID' ];

		$tabs[] = [
			'title' => button( 'add', '', '', 'smaller' ),
			'link' => 'Modules.php?modname=' . $_REQUEST['modname'] . '&table=new',
		];
	}
	else
	{
		$sql = "SELECT ID,TITLE,SORT_ORDER
		FROM attendance_code_categories
		WHERE SYEAR='" . UserSyear() . "'
		AND SCHOOL_ID='" . UserSchool() . "'
		ORDER BY SORT_ORDER IS NULL,SORT_ORDER,TITLE";

		$functions = [ 'TITLE' => '_makeTextInput', 'SORT_ORDER' => '_makeTextInput' ];

		$LO_columns = [ 'TITLE' => _( 'Title' ), 'SORT_ORDER' => _( 'Sort Order' ) ];

		$link['add']['html'] = [
			'TITLE' => _makeTextInput( '', 'TITLE' ),
			'SORT_ORDER' => _makeTextInput( '', 'SORT_ORDER' ),
		];

		$link['remove']['link'] = 'Modules.php?modname=' . $_REQUEST['modname'] . '&modfunc=remove&table=new';
		$link['remove']['variables'] = [ 'id' => 'ID' ];

		$tabs[] = [
			'title' => button( 'add', '', '', 'smaller' ),
			'link' => 'Modules.php?modname=' . $_REQUEST['modname'] . '&table=new',
		];
	}

	$LO_RET = DBGet( $sql, $functions );

	echo '<form action="' . URLEscape( 'Modules.php?modname=' . $_REQUEST['modname'] . '&modfunc=update&table=' . $_REQUEST['table']  ) . '" method="POST">';
	DrawHeader( '', SubmitButton() );
	echo '<br />';

	$LO_options = [
		'count' => false,
		'download' => false,
		'search' => false,
		'header' => WrapTabs( $tabs, 'Modules.php?modname=' . $_REQUEST['modname'] . '&table=' . $_REQUEST['table'] )
	];

//	ListOutput($LO_RET,$LO_columns,'.','.',$link,array(),array('count'=>false,'download'=>false,'search'=>false));
	ListOutput( $LO_RET, $LO_columns, '.', '.', $link, [], $LO_options );

	echo '<br /><div class="center">' . SubmitButton() . '</div>';
	echo '</form>';
}

/**
 * @param $value
 * @param $name
 */
function _makeTextInput( $value, $name )
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

	$extra = '';

	if ( $name === 'SORT_ORDER' )
	{
		$extra .= ' type="number" min="-9999" max="9999"';
	}
	elseif ( $name === 'SHORT_NAME' )
	{
		$extra .= 'size=5 maxlength=10';
	}
	elseif ( $name === 'TITLE' )
	{
		$extra .= 'maxlength=100';
	}

	if ( $id !== 'new'
		&& ( $name === 'TITLE'
			|| $name === 'SHORT_NAME' ) )
	{
		$extra .= ' required';
	}

	return TextInput( $value, 'values[' . $id . '][' . $name . ']', '', $extra );
}

/**
 * @param $value
 * @param $name
 */
function _makeSelectInput( $value, $name )
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

	if ( $name === 'TYPE' )
	{
		$options = [
			'teacher' => _( 'Teacher & Office' ),
			'official' => _( 'Office Only' ),
		];
	}
	elseif ( $name === 'STATE_CODE' )
	{
		$options = [
			'P' => _( 'Present' ),
			'A' => _( 'Absent' ),
			'H' => _( 'Half Day' ),
		];
	}

	return SelectInput(
		$value,
		'values[' . $id . '][' . $name . ']',
		'',
		$options,
		false
	);
}

/**
 * @param $value
 * @param $name
 */
function _makeCheckBoxInput( $value, $name )
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

	return CheckBoxInput(
		$value,
		'values[' . $id . '][' . $name . ']',
		'',
		'',
		( $id === 'new' )
	);
}
