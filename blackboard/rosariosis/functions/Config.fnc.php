<?php
/**
 * RosarioSIS & Program Configuration functions
 *
 * @package RosarioSIS
 * @subpackage functions
 */

/**
 * Get Configuration value
 * Insert or update (for current school) value if passed as argument.
 *
 * @example  Config( 'SYEAR' )
 *
 * @since 4.4 Add $value param to INSERT or UPDATE.
 * @since 6.0 Handle single quotes in $value with DBEscapeString().
 *
 * @global array  $_ROSARIO     Sets $_ROSARIO['Config']
 * @global string $DefaultSyear
 *
 * @param  string $item  Config title.
 * @param  string $value Value to INSERT or UPDATE. Defaults to null.
 *
 * @return string Config value
 */
function Config( $item, $value = null )
{
	global $_ROSARIO,
		$DefaultSyear;

	if ( ! $item )
	{
		return '';
	}

	// Get General & School Config.
	if ( ! isset( $_ROSARIO['Config'][ (string) $item ] ) )
	{
		$school_where = UserSchool() > 0 ?
			// If user logged in.
			"SCHOOL_ID='" . UserSchool() . "' OR SCHOOL_ID='0' ORDER BY SCHOOL_ID DESC" :
			// General (for every school) Config is stored with SCHOOL_ID=0.
			"SCHOOL_ID='0'";

		$_ROSARIO['Config'] = DBGet( "SELECT TITLE,CONFIG_VALUE,SCHOOL_ID
			FROM config
			WHERE " . $school_where, [], [ 'TITLE' ] );

		$_ROSARIO['Config']['SYEAR'][1]['CONFIG_VALUE'] = $DefaultSyear;
	}

	if ( ! is_null( $value ) )
	{
		$school_id = isset( $_ROSARIO['Config'][ (string) $item ][1]['SCHOOL_ID'] ) ?
			$_ROSARIO['Config'][ (string) $item ][1]['SCHOOL_ID'] :
			( UserSchool() > 0 ? UserSchool() : '0' );

		if ( ! isset( $_ROSARIO['Config'][ (string) $item ][1]['TITLE'] ) )
		{
			// Insert value (does not exist).
			DBQuery( "INSERT INTO config (CONFIG_VALUE,TITLE,SCHOOL_ID)
				VALUES('" . $value . "','" . $item . "','" . $school_id . "')" );
		}
		elseif ( $value != DBEscapeString( $_ROSARIO['Config'][ (string) $item ][1]['CONFIG_VALUE'] ) )
		{
			// Update value (different from current value).
			DBQuery( "UPDATE config
				SET CONFIG_VALUE='" . $value . "'
				WHERE TITLE='" . $item . "'
				AND SCHOOL_ID='" . (int) $school_id . "'" );
		}

		if ( $value !== DBEscapeString( $value ) )
		{
			$value = DBGetOne( "SELECT CONFIG_VALUE
				FROM config
				WHERE TITLE='" . $item . "'
				AND SCHOOL_ID='" . (int) $school_id . "'" );
		}

		$_ROSARIO['Config'][ (string) $item ][1]['CONFIG_VALUE'] = $value;
	}

	return issetVal( $_ROSARIO['Config'][ (string) $item ][1]['CONFIG_VALUE'] );
}


/**
 * Get Program Configuration
 * Get 1 value if item specified,
 * else get Program values
 * Insert or update value if passed as argument.
 *
 * Values set in School Configuration or directly in Module (ex.: Eligibility Entry times)
 *
 * @example if ( ProgramConfig( 'students', 'STUDENTS_SEMESTER_COMMENTS' ) )
 *
 * @since 2.9
 * @since 4.4 Add $value param to INSERT or UPDATE.
 * @since 6.0 Handle single quotes in $value with DBEscapeString().
 *
 * @global array        $_ROSARIO Sets $_ROSARIO['ProgramConfig']
 *
 * @param  string $program eligibility|grades|students|moodle|food_service|attendance... Program name.
 * @param  string $item    Program Config title (optional). Defaults to 'all'.
 * @param  string $value   Value to INSERT or UPDATE. Defaults to null.
 *
 * @return string|array Program Configuration value, or Program values in array
 */
function ProgramConfig( $program, $item = 'all', $value = null )
{
	global $_ROSARIO;

	if ( ! $program
		|| ! $item )
	{
		return '';
	}

	if ( ! isset( $_ROSARIO['ProgramConfig'][ (string) $program ] ) )
	{
		$_ROSARIO['ProgramConfig'] = DBGet( "SELECT PROGRAM,TITLE,VALUE
			FROM program_config
			WHERE SYEAR='" . UserSyear() . "'
			AND SCHOOL_ID='" . UserSchool() . "'", [], [ 'PROGRAM', 'TITLE' ] );
	}

	if ( ! is_null( $value )
		&& $item !== 'all' )
	{
		if ( ! isset( $_ROSARIO['ProgramConfig'][ (string) $program ][ (string) $item ][1]['TITLE'] ) )
		{
			// Insert value (does not exist).
			DBQuery( "INSERT INTO program_config (VALUE,PROGRAM,TITLE,SCHOOL_ID,SYEAR)
				VALUES('" . $value . "','" . $program . "','" . $item . "','" .
				UserSchool() . "','" . UserSyear() . "')" );

			$_ROSARIO['ProgramConfig'][ (string) $program ][ (string) $item ][1]['TITLE'] = $item;
		}
		elseif ( $value != DBEscapeString( $_ROSARIO['ProgramConfig'][ (string) $program ][ (string) $item ][1]['VALUE'] ) )
		{
			// Update value (different from current value).
			DBQuery( "UPDATE program_config
				SET VALUE='" . $value . "'
				WHERE TITLE='" . $item . "'
				AND SCHOOL_ID='" . UserSchool() . "'
				AND SYEAR='" . UserSyear() . "'" );
		}

		if ( $value !== DBEscapeString( $value ) )
		{
			$value = DBGetOne( "SELECT VALUE
				FROM program_config
				WHERE TITLE='" . $item . "'
				AND SCHOOL_ID='" . UserSchool() . "'
				AND SYEAR='" . UserSyear() . "'" );
		}

		$_ROSARIO['ProgramConfig'][ (string) $program ][ (string) $item ][1]['VALUE'] = $value;
	}

	if ( $item === 'all' )
	{
		return issetVal( $_ROSARIO['ProgramConfig'][ (string) $program ] );
	}

	return issetVal( $_ROSARIO['ProgramConfig'][ (string) $program ][ (string) $item ][1]['VALUE'] );
}



/**
 * Program User Config
 * To get all config options at once
 * If you want only one option, prefer `Preferences()`
 * Insert or update values if passed as argument.
 *
 * @example $gradebook_config = ProgramUserConfig( 'Gradebook' );
 *
 * @see Preferences()
 * @see program_user_config table
 *
 * @since 2.9
 * @since 4.4 Add $values param to INSERT or UPDATE.
 * @since 5.8 Set $staff_id to -1 to override user config.
 * @since 6.0 Handle single quotes in $value with DBEscapeString().
 * @since 8.0 Fix SQL error when $staff_id is 0 (no user in session).
 * @since 8.7 Always return array, not null.
 *
 * @param string  $program  Gradebook|WidgetsSearch|StaffWidgetsSearch|
 * @param integer $staff_id Staff ID (optional). Defaults to User( 'STAFF_ID' ).
 * @param array   $values   Values to INSERT or UPDATE. Defaults to null.
 *
 * @return array Program User Config, associative array( '[title]' => '[value]' ).
 */
function ProgramUserConfig( $program, $staff_id = 0, $values = null )
{
	static $program_config;

	if ( ! $program )
	{
		return [];
	}

	$staff_id = $staff_id ? (int) $staff_id : User( 'STAFF_ID' );

	if ( ! isset( $program_config[ $program ][ $staff_id ] ) )
	{
		$config_RET = DBGet( "SELECT TITLE,VALUE
			FROM program_user_config
			WHERE (USER_ID='" . (int) $staff_id . "' OR USER_ID='-1')
			AND PROGRAM='" . $program . "'
			ORDER BY USER_ID", [], [ 'TITLE' ] );

		$program_config[ $program ][ $staff_id ] = array();

		foreach ( $config_RET as $title => $value )
		{
			$program_config[ $program ][ $staff_id ][ $title ] = $value[1]['VALUE'];
		}
	}

	if ( is_array( $values )
		&& $staff_id )
	{
		foreach ( $values as $title => $value )
		{
			if ( empty( $title ) && $title != '0' )
			{
				// TITLE column is NOT NULL.
				continue;
			}

			if ( ! array_key_exists( $title, (array) $program_config[ $program ][ $staff_id ] ) )
			{
				// Insert value (does not exist).
				DBQuery( "INSERT INTO program_user_config (VALUE,PROGRAM,TITLE,USER_ID)
					VALUES('" . $value . "','" . $program . "','" . $title . "','" .
					$staff_id . "')" );
			}
			elseif ( $value != DBEscapeString( $program_config[ $program ][ $staff_id ][ $title ] ) )
			{
				// Update value (different from current value).
				DBQuery( "UPDATE program_user_config
					SET VALUE='" . $value . "'
					WHERE TITLE='" . $title . "'
					AND PROGRAM='" . $program . "'
					AND USER_ID='" . (int) $staff_id . "'" );
			}

			if ( $value !== DBEscapeString( $value ) )
			{
				$value = str_replace( "''", "'", $value );
			}

			$program_config[ $program ][ $staff_id ][ $title ] = $value;
		}
	}

	return $program_config[ $program ][ $staff_id ];
}
