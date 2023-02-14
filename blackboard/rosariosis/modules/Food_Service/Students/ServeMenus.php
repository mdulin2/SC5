<?php
require_once 'modules/Food_Service/includes/FS_Icons.inc.php';
require_once 'ProgramFunctions/TipMessage.fnc.php';

Widgets( 'fsa_status_active' );
Widgets( 'fsa_barcode' );

Search( 'student_id', $extra );

if ( $_REQUEST['modfunc'] === 'submit' )
{
	if ( ! empty( $_REQUEST['submit']['cancel'] ) )
	{
		if ( DeletePrompt( _( 'Sale' ), _( 'Cancel' ) ) )
		{
			unset( $_SESSION['FSA_sale'] );

			// Unset modfunc & redirect URL.
			RedirectURL( 'modfunc' );
		}
	}
	elseif ( $_REQUEST['submit']['save']
		&& ! empty( $_SESSION['FSA_sale'] ) )
	{
		$student = DBGet( "SELECT ACCOUNT_ID,DISCOUNT
			FROM food_service_student_accounts
			WHERE STUDENT_ID='" . UserStudentID() . "'" );

		$student = $student[1];

		$fields = 'ACCOUNT_ID,STUDENT_ID,SYEAR,SCHOOL_ID,DISCOUNT,BALANCE,' . DBEscapeIdentifier( 'TIMESTAMP' ) . ',SHORT_NAME,DESCRIPTION,SELLER_ID';

		$values = "'" . $student['ACCOUNT_ID'] . "','" . UserStudentID() . "','" .
			UserSyear() . "','" . UserSchool() . "','" . $discount .
			"',(SELECT BALANCE FROM food_service_accounts WHERE ACCOUNT_ID='" . (int) $student['ACCOUNT_ID'] .
			"'),CURRENT_TIMESTAMP,'" . $menus_RET[$_REQUEST['menu_id']][1]['TITLE'] . "','" .
			$menus_RET[$_REQUEST['menu_id']][1]['TITLE'] . ' - ' . DBDate() . "','" . User( 'STAFF_ID' ) . "'";

		$sql = "INSERT INTO food_service_transactions (" . $fields . ") values (" . $values . ")";

		DBQuery( $sql );

		$transaction_id = DBLastInsertID();

		$items_RET = DBGet( "SELECT DESCRIPTION,SHORT_NAME,PRICE,PRICE_REDUCED,PRICE_FREE
			FROM food_service_items
			WHERE SCHOOL_ID='" . UserSchool() . "'", [], [ 'SHORT_NAME' ] );

		$item_id = 0;

		foreach ( (array) $_SESSION['FSA_sale'] as $item_sn )
		{
			// determine price based on discount
			$price = $items_RET[$item_sn][1]['PRICE'];
			$discount = $student['DISCOUNT'];

			if ( $student['DISCOUNT'] == 'Reduced' )
			{
				if ( $items_RET[$item_sn][1]['PRICE_REDUCED'] != '' )
				{
					$price = $items_RET[$item_sn][1]['PRICE_REDUCED'];
				}
				else
				{
					$discount = '';
				}
			}
			elseif ( $student['DISCOUNT'] == 'Free' )
			{
				if ( $items_RET[$item_sn][1]['PRICE_FREE'] != '' )
				{
					$price = $items_RET[$item_sn][1]['PRICE_FREE'];
				}
				else
				{
					$discount = '';
				}
			}

			$fields = 'ITEM_ID,TRANSACTION_ID,AMOUNT,DISCOUNT,SHORT_NAME,DESCRIPTION';

			$values = "'" . $item_id++ . "','" . $transaction_id . "','-" . $price . "','" . $discount . "','" . $items_RET[$item_sn][1]['SHORT_NAME'] . "','" . $items_RET[$item_sn][1]['DESCRIPTION'] . "'";

			$sql = "INSERT INTO food_service_transaction_items (" . $fields . ") values (" . $values . ")";

			DBQuery( $sql );
		}

		DBQuery( "UPDATE food_service_accounts
			SET TRANSACTION_ID='" . (int) $transaction_id . "',BALANCE=BALANCE+(SELECT sum(AMOUNT)
				FROM food_service_transaction_items
				WHERE TRANSACTION_ID='" . (int) $transaction_id . "')
			WHERE ACCOUNT_ID='" . (int) $student['ACCOUNT_ID'] . "'" );

		unset( $_SESSION['FSA_sale'] );

		// Unset modfunc & redirect URL.
		RedirectURL( 'modfunc' );
	}
	else
	{
		// Unset modfunc & redirect URL.
		RedirectURL( 'modfunc' );
	}

	// Unset submit & redirect URL.
	RedirectURL( 'submit' );
}

if ( UserStudentID() && ! $_REQUEST['modfunc'] )
{
	$student = DBGet( "SELECT s.STUDENT_ID," . DisplayNameSQL( 's' ) . " AS FULL_NAME,
	fsa.ACCOUNT_ID,fsa.STATUS,fsa.DISCOUNT,fsa.BARCODE,
	(SELECT BALANCE FROM food_service_accounts WHERE ACCOUNT_ID=fsa.ACCOUNT_ID) AS BALANCE
	FROM students s,food_service_student_accounts fsa
	WHERE s.STUDENT_ID='" . UserStudentID() . "'
	AND fsa.STUDENT_ID=s.STUDENT_ID" );

	$student = $student[1];

	echo '<form action="' . URLEscape( 'Modules.php?modname=' . $_REQUEST['modname'] . '&modfunc=submit&menu_id=' . $_REQUEST['menu_id']  ) . '" method="POST">';

	DrawHeader(
		'',
		SubmitButton( _( 'Cancel Sale' ), 'submit[cancel]', '' ) . // No .primary button class.
		SubmitButton( _( 'Complete Sale' ), 'submit[save]' )
	);

	echo '</form>';

	$student_name_photo = MakeStudentPhotoTipMessage( $student['STUDENT_ID'], $student['FULL_NAME'] );

	DrawHeader(
		NoInput( $student_name_photo, $student['STUDENT_ID'] ),
		NoInput( red( $student['BALANCE'] ), _( 'Balance' ) )
	);

	if ( $student['BALANCE'] != '' )
	{
		// @since 9.0 Add Food Service icon to list.
		$functions = [ 'ICON' => 'makeIcon' ];

		$RET = DBGet( "SELECT fsti.DESCRIPTION,fsti.AMOUNT,
			(SELECT ICON FROM food_service_items WHERE SHORT_NAME=fsti.SHORT_NAME LIMIT 1) AS ICON
			FROM food_service_transactions fst,food_service_transaction_items fsti
			WHERE fst.ACCOUNT_ID='" . (int) $student['ACCOUNT_ID'] . "'
			AND fst.STUDENT_ID='" . UserStudentID() . "'
			AND fst.SYEAR='" . UserSyear() . "'
			AND fst.SHORT_NAME='" . $menus_RET[$_REQUEST['menu_id']][1]['TITLE'] . "'
			AND fst.TIMESTAMP BETWEEN CURRENT_DATE AND 'tomorrow'
			AND fsti.TRANSACTION_ID=fst.TRANSACTION_ID", $functions );

		$columns = [
			'DESCRIPTION' => _( 'Item' ),
			'ICON' => _( 'Icon' ),
			'AMOUNT' => _( 'Amount' ),
		];

		$singular = sprintf( _( 'Earlier %s Sale' ), $menus_RET[$_REQUEST['menu_id']][1]['TITLE'] );

		$plural = sprintf( _( 'Earlier %s Sales' ), $menus_RET[$_REQUEST['menu_id']][1]['TITLE'] );

		ListOutput( $RET, $columns, $singular, $plural, [], false, [ 'save' => false, 'search' => false ] );

		$items_RET = DBGet( "SELECT fsi.SHORT_NAME,fsi.DESCRIPTION,fsi.PRICE,fsi.PRICE_REDUCED,fsi.PRICE_FREE,fsi.ICON
		FROM food_service_items fsi,food_service_menu_items fsmi
		WHERE fsmi.MENU_ID='" . (int) $_REQUEST['menu_id'] . "'
		AND fsi.ITEM_ID=fsmi.ITEM_ID
		AND fsmi.CATEGORY_ID IS NOT NULL
		AND fsi.SCHOOL_ID='" . UserSchool() . "'
		ORDER BY fsi.SORT_ORDER IS NULL,fsi.SORT_ORDER", [ 'ICON' => 'makeIcon' ], [ 'SHORT_NAME' ] );
		$items = [];

		foreach ( (array) $items_RET as $sn => $item )
		{
			$items += [ $sn => $item[1]['DESCRIPTION'] ];
		}

		$LO_ret = [ [] ];
		//FJ fix error Warning: Invalid argument supplied for foreach()

		if ( isset( $_SESSION['FSA_sale'] ) && is_array( $_SESSION['FSA_sale'] ) )
		{
			foreach ( (array) $_SESSION['FSA_sale'] as $id => $item_sn )
			{
				// determine price based on discount
				$price = $items_RET[$item_sn][1]['PRICE'];

				if ( $student['DISCOUNT'] == 'Reduced' )
				{
					if ( $items_RET[$item_sn][1]['PRICE_REDUCED'] != '' )
					{
						$price = $items_RET[$item_sn][1]['PRICE_REDUCED'];
					}
				}
				elseif ( $student['DISCOUNT'] == 'Free' )
				{
					if ( $items_RET[$item_sn][1]['PRICE_FREE'] != '' )
					{
						$price = $items_RET[$item_sn][1]['PRICE_FREE'];
					}
				}

				$LO_ret[] = [ 'SALE_ID' => $id, 'PRICE' => $price, 'DESCRIPTION' => $items_RET[$item_sn][1]['DESCRIPTION'], 'ICON' => $items_RET[$item_sn][1]['ICON'] ];
			}
		}

		unset( $LO_ret[0] );

		$link['remove'] = [ 'link' => 'Modules.php?modname=' . $_REQUEST['modname'] . '&modfunc=remove&menu_id=' . $_REQUEST['menu_id'],
			'variables' => [ 'id' => 'SALE_ID' ] ];

		//		$link['add']['html'] = array('DESCRIPTION' => '<table class="cellspacing-0"><tr><td>'.SelectInput('','item_sn','',$items).'</td></tr></table>','ICON' => '<table class="cellspacing-0"><tr><td><input type=submit value='._('Add').'></td></tr></table>','remove'=>button('add'));
		$link['add']['html'] = [
			'DESCRIPTION' => SelectInput( '', 'item_sn', '', $items ),
			'ICON' => SubmitButton( _( 'Add' ) ),
			'PRICE' => '&nbsp;',
			'remove' => button( 'add' ),
		];

		$columns = [ 'DESCRIPTION' => _( 'Item' ), 'ICON' => _( 'Icon' ), 'PRICE' => _( 'Price' ) ];

		$tabs = [];

		foreach ( (array) $menus_RET as $id => $menu )
		{
			$tabs[] = [ 'title' => $menu[1]['TITLE'], 'link' => 'Modules.php?modname=' . $_REQUEST['modname'] . '&menu_id=' . $id ];
		}

		$extra = [
			'save' => false,
			'search' => false,
			'header' => WrapTabs( $tabs, 'Modules.php?modname=' . $_REQUEST['modname'] . '&menu_id=' . $_REQUEST['menu_id'] ),
		];

		echo '<br />';
		echo '<form action="' . URLEscape( 'Modules.php?modname=' . $_REQUEST['modname'] . '&modfunc=add&menu_id=' . $_REQUEST['menu_id']  ) . '" method="POST">';

		ListOutput( $LO_ret, $columns, 'Item', 'Items', $link, [], $extra );

		echo '</form>';
	}
	else
	{
		ErrorMessage( [ _( 'This student does not have a valid Meal Account.' ) ], 'fatal' );
	}
}
