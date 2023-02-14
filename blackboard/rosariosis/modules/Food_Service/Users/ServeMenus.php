<?php
require_once 'modules/Food_Service/includes/FS_Icons.inc.php';
require_once 'ProgramFunctions/TipMessage.fnc.php';

StaffWidgets( 'fsa_status_active' );
StaffWidgets( 'fsa_barcode' );
StaffWidgets( 'fsa_exists_Y' );

Search( 'staff_id', $extra );

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
		$fields = 'STAFF_ID,SYEAR,SCHOOL_ID,BALANCE,' . DBEscapeIdentifier( 'TIMESTAMP' ) . ',SHORT_NAME,DESCRIPTION,SELLER_ID';

		$values = "'" . UserStaffID() . "','" . UserSyear() . "','" . UserSchool() .
			"',(SELECT BALANCE
			FROM food_service_staff_accounts
			WHERE STAFF_ID='" . UserStaffID() . "'),CURRENT_TIMESTAMP,'" .
			$menus_RET[$_REQUEST['menu_id']][1]['TITLE'] . "','" .
			$menus_RET[$_REQUEST['menu_id']][1]['TITLE'] . ' - ' . DBDate() . "','" . User( 'STAFF_ID' ) . "'";

		$sql = "INSERT INTO food_service_staff_transactions (" . $fields . ") values (" . $values . ")";

		DBQuery( $sql );

		$transaction_id = DBLastInsertID();

		$items_RET = DBGet( "SELECT DESCRIPTION,SHORT_NAME,PRICE_STAFF
			FROM food_service_items
			WHERE SCHOOL_ID='" . UserSchool() . "'", [], [ 'SHORT_NAME' ] );

		$item_id = 0;

		foreach ( (array) $_SESSION['FSA_sale'] as $item_sn )
		{
			$price = $items_RET[$item_sn][1]['PRICE_STAFF'];

			$fields = 'ITEM_ID,TRANSACTION_ID,AMOUNT,SHORT_NAME,DESCRIPTION';

			$values = "'" . $item_id++ . "','" . $transaction_id . "','-" . $price . "','" . $items_RET[$item_sn][1]['SHORT_NAME'] . "','" . $items_RET[$item_sn][1]['DESCRIPTION'] . "'";

			$sql = "INSERT INTO food_service_staff_transaction_items (" . $fields . ") values (" . $values . ")";

			DBQuery( $sql );
		}

		$sql = "UPDATE food_service_staff_accounts
			SET TRANSACTION_ID='" . (int) $transaction_id . "',BALANCE=BALANCE+(SELECT sum(AMOUNT)
				FROM food_service_staff_transaction_items
				WHERE TRANSACTION_ID='" . (int) $transaction_id . "')
			WHERE STAFF_ID='" . UserStaffID() . "'";

		DBQuery( $sql );

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

if ( UserStaffID()
	&& ! $_REQUEST['modfunc'] )
{
	$staff = DBGet( "SELECT s.STAFF_ID," . DisplayNameSQL( 's' ) . " AS FULL_NAME,
	(SELECT STAFF_ID FROM food_service_staff_accounts WHERE STAFF_ID=s.STAFF_ID) AS ACCOUNT_ID,
	(SELECT BALANCE FROM food_service_staff_accounts WHERE STAFF_ID=s.STAFF_ID) AS BALANCE
	FROM staff s
	WHERE s.STAFF_ID='" . UserStaffID() . "'" );

	$staff = $staff[1];

	echo '<form action="' . URLEscape( 'Modules.php?modname=' . $_REQUEST['modname'] . '&modfunc=submit&menu_id=' . $_REQUEST['menu_id']  ) . '" method="POST">';

	DrawHeader(
		'',
		SubmitButton( _( 'Cancel Sale' ), 'submit[cancel]', '' ) . // No .primary button class.
		SubmitButton( _( 'Complete Sale' ), 'submit[save]' )
	);

	echo '</form>';

	$staff_name_photo = MakeUserPhotoTipMessage( $staff['STAFF_ID'], $staff['FULL_NAME'] );

	DrawHeader(
		NoInput( $staff_name_photo, $staff['STAFF_ID'] ),
		NoInput( red( $staff['BALANCE'] ), _( 'Balance' ) )
	);

	if ( $staff['ACCOUNT_ID'] && $staff['BALANCE'] != '' )
	{
		// @since 9.0 Add Food Service icon to list.
		$functions = [ 'ICON' => 'makeIcon' ];

		$RET = DBGet( "SELECT fsti.DESCRIPTION,fsti.AMOUNT,
		(SELECT ICON FROM food_service_items WHERE SHORT_NAME=fsti.SHORT_NAME LIMIT 1) AS ICON
		FROM food_service_staff_transactions fst,food_service_staff_transaction_items fsti
		WHERE fst.STAFF_ID='" . UserStaffID() . "'
		AND fst.SYEAR='" . UserSyear() . "'
		AND fst.SHORT_NAME='" . $menus_RET[$_REQUEST['menu_id']][1]['TITLE'] . "'
		AND fst.TIMESTAMP BETWEEN CURRENT_DATE
		AND (CURRENT_DATE + INTERVAL " . ( $DatabaseType === 'mysql' ? '1 DAY' : "'1 DAY'" ) . ")
		AND fsti.TRANSACTION_ID=fst.TRANSACTION_ID", $functions );

		$columns = [
			'DESCRIPTION' => _( 'Item' ),
			'ICON' => _( 'Icon' ),
			'AMOUNT' => _( 'Amount' ),
		];

		$singular = sprintf( _( 'Earlier %s Sale' ), $menus_RET[$_REQUEST['menu_id']][1]['TITLE'] );
		$plural = sprintf( _( 'Earlier %s Sales' ), $menus_RET[$_REQUEST['menu_id']][1]['TITLE'] );

		ListOutput( $RET, $columns, $singular, $plural, [], false, [ 'save' => false, 'search' => false ] );

		$items_RET = DBGet( "SELECT fsi.SHORT_NAME,fsi.DESCRIPTION,fsi.PRICE_STAFF,fsi.ICON
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

		if ( isset( $_SESSION['FSA_sale'] ) )
		{
			foreach ( (array) $_SESSION['FSA_sale'] as $id => $item_sn )
			{
				$price = $items_RET[$item_sn][1]['PRICE_STAFF'];
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
			$tabs[] = [
				'title' => $menu[1]['TITLE'],
				'link' => 'Modules.php?modname=' . $_REQUEST['modname'] . '&menu_id=' . $id,
			];
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
		ErrorMessage( [ _( 'This user does not have a Food Service Account.' ) ], 'fatal' );
	}
}
