<?php
/**
 * Lists / Listings
 *
 * @package RosarioSIS
 * @subpackage functions
 *
 * @since 4.0 Add List Before and After action hooks
 */

function ListOutput( $result, $column_names, $singular = '.', $plural = '.', $link = [], $group = [], $options = [] )
{
	$default_options = [
		'save' => '1',
		'search' => true,
		'center' => true,
		'count' => true,
		'sort' => empty( $group ),
		'header_color' => Preferences( 'HEADER' ),
		'responsive' => true,
		'add' => true,
	];

	$options = empty( $options ) ?
		$default_options :
		array_replace_recursive( $default_options, $options );

	$LO_page = issetVal( $_REQUEST['LO_page'], '' );

	// FJ bugfix ListOutput sorting when more than one list in a page.
	$LO_sort = issetVal( $_REQUEST['LO_sort'], '' );

	$LO_dir = issetVal( $_REQUEST['LO_dir'], '' );

	$LO_search = issetVal( $_REQUEST['LO_search'], '' );

	$LO_save = issetVal( $_REQUEST['LO_save'], '' );

	if ( ! $options['add']
		|| ! AllowEdit()
		|| isset( $_REQUEST['_ROSARIO_PDF'] ) )
	{
		if ( ! empty( $link ) )
		{
			unset( $link['add'] );
			unset( $link['remove'] );
		}
	}

	$result_count = $display_count = count( (array) $result );

	if ( $result_count > 1000 )
	{
		// Limit to 1000!
		$result_count = 1000;

		// Remove results above 1000.
		$result = array_slice( $result, 0, 1000, true );
	}

	$num_displayed = 1000;

	// PREPARE LINKS ---.
	$extra = URLEscape( 'LO_page=' . $LO_page .
		'&LO_sort=' . $LO_sort .
		'&LO_dir=' . $LO_dir .
		'&LO_search=' . $LO_search );

	$PHP_tmp_SELF = PreparePHP_SELF(
		$_REQUEST,
		[
			'LO_page',
			'LO_sort',
			'LO_dir',
			'LO_search',
			'LO_save',
		]
	);

	// END PREPARE LINKS ---.

	// UN-GROUPING
	$group_count = empty( $group ) ? false : count( $group );

	if ( $group_count
		&& $result_count )
	{
		$group_result = $result;

		unset( $result );

		$result[0] = '';

		foreach ( (array) $group_result as $item1 )
		{
			foreach ( (array) $item1 as $item2 )
			{
				if ( $group_count == 1 )
				{
					$result[] = $item2;

					continue;
				}

				foreach ( (array) $item2 as $item3 )
				{
					if ( $group_count == 2 )
					{
						$result[] = $item3;

						continue;
					}

					foreach ( (array) $item3 as $item4 )
					{
						$result[] = $item4;
					}
				}
			}
		}

		unset( $result[0] );

		$result_count = count( $result );
	}
	// END UN-GROUPING

	$display_zero = false;

	// PRINT HEADINGS, PREPARE PDF, AND SORT THE LIST ---.
	if ( $result_count != 0 )
	{
		$count = $remove = 0;

		if ( isset( $link['remove']['variables'] ) )
		{
			$remove = count( $link['remove']['variables'] );
		}

		$cols = count( $column_names );

		// HANDLE SEARCHES ---.
		if ( $result_count
			&& $options['search']
			&& $LO_search !== '' )
		{
			// @since 5.8.
			$result = _listSearch( $result, $LO_search );

			$result_count = $display_count = count( $result );

			if ( $result_count )
			{
				$column_names['RELEVANCE'] = _( 'Relevance' );
			}

			if ( is_array( $group )
				&& count( $group ) )
			{
				$options['count'] = false;

				$display_zero = true;
			}
		}

		// END SEARCHES ---.

		if ( $LO_sort
			&& isset( $result[1][$LO_sort] ) )
		{
			foreach ( (array) $result as $sort )
			{
				if ( mb_substr( (string) $sort[$LO_sort], 0, 4 ) != '<!--' )
				{
					//FJ better list sorting by isolating the values
					//$sort_array[] = $sort[ $LO_sort ];
					$sort_array[] = strip_tags( preg_replace(
						'/<script\b[^>]*>(.*?)<\/script>/is',
						"",
						(string) $sort[$LO_sort]
					) );

					continue;
				}

				// Use value inside comment to sort!
				$sort_array[] = trim( mb_substr(
					$sort[$LO_sort],
					4,
					mb_strpos( $sort[$LO_sort], '-->' ) - 4
				) );
			}

			$dir = $LO_dir == -1 ? SORT_DESC: SORT_ASC;

			if ( $result_count > 1 )
			{
				if ( is_int( $sort_array[1] )
					|| is_double( $sort_array[1] ) )
				{
					array_multisort( $sort_array, $dir, SORT_NUMERIC, $result );
				}
				else
				{
					array_multisort( $sort_array, $dir, $result );
				}

				array_unshift( $result, [ 'always_start_list_at_key_1' ] );

				unset( $result[0] );
			}
		}
	}

	// List Before hook.
	do_action( 'functions/ListOutput.fnc.php|list_before' );

	// HANDLE SAVING THE LIST ---.

	if ( $options['save']
		&& (int) $LO_save === (int) $options['save']
		&& ! headers_sent() )
	{
		_listSave( $result, $column_names, $singular, $plural, Preferences( 'DELIMITER' ) );
	}

	// END SAVING THE LIST ---.

	if ( $result_count > 0
		|| $LO_search !== '' )
	{
		if ( empty( $LO_dir ) )
		{
			$LO_dir = 1;
		}

		// HANDLE MISC ---.

		if ( ! isset( $_REQUEST['_ROSARIO_PDF'] ) )
		{
			if ( empty( $LO_page )
				|| (string) (int) $LO_page != $LO_page
				|| $LO_page < 1 )
			{
				$LO_page = 1;
			}

			$start = ( $LO_page - 1 ) * $num_displayed + 1;
			$stop = $start + ( $num_displayed - 1 );

			if ( $stop > $result_count )
			{
				$stop = $result_count;
			}

			if ( $result_count >= $num_displayed )
			{
				$where_message = ' <span class="size-1">' .
					sprintf( _( 'Displaying %d through %d' ), $start, $stop ) . '</span>';
			}
		}
		else
		{
			$start = 1;
			$stop = $result_count;

			if ( $cols > 8 || ! empty( $_REQUEST['expanded_view'] ) )
			{
				// For wkhtmltopdf.
				$_SESSION['orientation'] = 'landscape';
			}
		}

		// END MISC ---.
	}

	$class = '';

	if ( $plural && $plural !== '.' )
	{
		$class = mb_strtolower( preg_replace(
			'/([^\-a-z\/0-9]+)/i',
			'-',
			$plural
		) );
	}

	echo '<div class="list-outer ' . $class . '">';

	// SEARCH BOX & MORE HEADERS ---.

	if ( ! empty( $options['header'] ) )
	{
		echo '<table class="postbox width-100p cellspacing-0 list-header"><thead><tr><th class="center">' .
			$options['header'] . '</th></tr></thead></table>
			<div class="postbox">';
	}

	$list_has_nav = false;

	if ( $options['count']
		|| $display_zero
		|| ( $options['save']
			|| $options['search']
			&& ! isset( $_REQUEST['_ROSARIO_PDF'] ) ) )
	{
		$list_has_nav = true;

		echo '<table class="list-nav"><tr class="st"><td>';

		$has_count_text = false;

		if ( $singular !== '.'
			&& $plural !== '.'
			&& $options['count'] )
		{
			if ( $display_count > 0 )
			{
				$result_text = ngettext( $singular, $plural, $display_count );

				echo '<span class="size-1">' . sprintf(
					ngettext( '%d %s was found.', '%d %s were found.', $display_count ),
					$display_count,
					mb_strtolower( $result_text )
				) . '</span>';
			}

			echo empty( $where_message ) ? '' : $where_message;

			$has_count_text = true;
		}

		if (  ( $options['count']
			|| $display_zero )
			&& ( $result_count == 0
				|| $display_count == 0 ) )
		{
			$result_text = ngettext(
				( $singular === '.' ? _( 'Result' ) : $singular ),
				( $plural === '.' ? _( 'Results' ) : $plural ),
				0
			);

			// No results message. Default to "Results".
			echo '<b class="size-1">' . sprintf(
				_( 'No %s were found.' ),
				mb_strtolower( $result_text )
			) . '</b>';

			$has_count_text = true;
		}

		if ( $options['save']
			&& ! isset( $_REQUEST['_ROSARIO_PDF'] )
			&& $result_count > 0 )
		{
			echo $has_count_text ? '&nbsp;' : '';

			// Save / Export list button.
			echo '<a href="' . $PHP_tmp_SELF . '&amp;' . $extra .
			'&amp;LO_save=' . $options['save'] .
			'&amp;_ROSARIO_PDF=true" target="_blank"><img src="assets/themes/' .
			Preferences( 'THEME' ) . '/btn/download.png" class="alignImg" title="' .
			AttrEscape( _( 'Export list' ) ) . '" alt="' . AttrEscape( _( 'Export list' ) ) . '" /></a>';
		}

		echo '</td>';

		$colspan = 1;

		if ( $options['search']
			&& ! isset( $_REQUEST['_ROSARIO_PDF'] )
			&& ( $result_count > 0
				|| $LO_search ) )
		{
			echo '<td class="align-right">';

			// Do not remove search URL due to document.URL = 'index.php' in old IE browsers.
			$search_URL = PreparePHP_SELF( $_REQUEST, [ 'LO_search' ] );

			$onkeypress_js = 'LOSearch(event, this.value, ' . json_encode( $search_URL ) . ');';

			$onclick_js = 'LOSearch(event, $(\'#LO_search\').val(), ' . json_encode( $search_URL ) . ');';

			echo '<input type="text" id="LO_search" name="LO_search" value="' .
			AttrEscape( DBUnescapeString( $LO_search ) ) .
			'" placeholder="' . AttrEscape( _( 'Search' ) ) .
			'" onkeypress="' . AttrEscape( $onkeypress_js ) . '" autocomplete="off" />
				<img src="assets/themes/' . Preferences( 'THEME' ) . '/btn/visualize.png"
				onclick="' . AttrEscape( $onclick_js ) . '"
				class="button" alt="" title="' . AttrEscape( _( 'Search' ) ) . '" />
				<label for="LO_search" class="a11y-hidden">' . _( 'Search' ) . '</label>';

			echo '</td>';

			$colspan++;
		}

		echo '</tr></table>';
	}

	// END SEARCH BOX & MORE HEADERS ---.

	if ( $result_count > 0 )
	{
		echo '<div class="list-wrapper"><table class="list widefat' .
			( $options['responsive'] && ! isset( $_REQUEST['_ROSARIO_PDF'] ) ? ' rt' : '' ) .
			( ! $list_has_nav ? ' list-no-nav' : '' ) . '"><thead><tr>';

		$i = 1;

		if ( $remove
			&& ! isset( $_REQUEST['_ROSARIO_PDF'] ) )
		{
			echo '<th><span class="a11y-hidden">' . _( 'Delete' ) . '</span></th>';

			$i++;
		}

		if ( $cols )
		{
			foreach ( (array) $column_names as $key => $value )
			{
				$direction = $LO_sort == $key ? -1 * (int) $LO_dir : 1;

				$i++;

				if ( isset( $_REQUEST['_ROSARIO_PDF'] ) )
				{
					echo '<td style="background-color:' . $options['header_color'] . '; color:#fff;"><b>' .
						ParseMLField( $value ) . '</b></td>';

					continue;
				}

				if ( $options['sort']
					// Fix MakeChooseCheckbox() remove parent link to sort column
					&& mb_strpos( $value, 'id="controller"' ) === false )
				{
					echo '<th><a href="' . $PHP_tmp_SELF . URLEscape( '&LO_page=' . $LO_page .
						'&LO_sort=' . $key . '&LO_dir=' . $direction .
						'&LO_search=' . issetVal( $LO_search, '' ) ) . '">' .
						ParseMLField( $value ) . '</a></th>';

					continue;
				}

				echo '<th>' . ParseMLField( $value ) . '</th>';
			}
		}

		echo '</tr></thead><tbody>';

		// mab - enable add link as first or last

		if ( isset( $link['add']['first'] )
			&& ( $stop - $start + 1 ) >= $link['add']['first'] )
		{
			if ( $link['add']['link'] && ! isset( $_REQUEST['_ROSARIO_PDF'] ) )
			{
				echo '<tr><td colspan="' . ( $remove ? $cols + 1 : $cols ) . '">' .
					button(
						'add',
						issetVal( $link['add']['title'], '' ),
						( mb_strpos( $link['add']['link'], '"' ) === 0 ?
							$link['add']['link'] :
							'"' . URLEscape( $link['add']['link'] ) . '"' )
					) . '</td></tr>';
			}
			elseif ( $link['add']['span'] && ! isset( $_REQUEST['_ROSARIO_PDF'] ) )
			{
				echo '<tr><td colspan="' . ( $remove ? $cols + 1 : $cols ) . '">' .
					button( 'add' ) . $link['add']['span'] . '</td></tr>';
			}
			elseif ( $link['add']['html'] && $cols )
			{
				echo '<tr>';

				if ( $remove && ! isset( $_REQUEST['_ROSARIO_PDF'] ) && $link['add']['html']['remove'] )
				{
					echo '<td>' . $link['add']['html']['remove'] . '</td>';
				}
				elseif ( $remove && ! isset( $_REQUEST['_ROSARIO_PDF'] ) )
				{
					echo '<td>' . button( 'add' ) . '</td>';
				}

				foreach ( (array) $column_names as $key => $value )
				{
					echo '<td>' . $link['add']['html'][$key] . '</td>';
				}

				echo '</tr>';

				$count++;
			}
		}

		for ( $i = $start; $i <= $stop; $i++ )
		{
			$item = $result[$i];

			if ( isset( $_REQUEST['_ROSARIO_PDF'] ) && count( $item ) )
			{
				$key = array_keys( $item );
				$size = count( $key );

				for ( $j = 0; $j < $size; $j++ )
				{
					if ( empty( $item[$key[$j]] ) )
					{
						continue;
					}

					$value = preg_replace( '!<select.*selected\>([^<]+)<.*</select\>!i', '\\1', $item[$key[$j]] );
					$value = preg_replace( '!<select.*</select\>!i', '', $value );
					$item[$key[$j]] = preg_replace( "/<div onclick=[^']+'>/", '', $value );
				}
			}

			echo '<tr>';

			$count++;

			if ( $remove && ! isset( $_REQUEST['_ROSARIO_PDF'] ) )
			{
				$button_title = issetVal( $link['remove']['title'] );

				$button_link = empty( $link['remove']['link'] ) ?
					PreparePHP_SELF( [], array_keys( $link['remove']['variables'] ) ) :
					URLEscape( $link['remove']['link'] );

				foreach ( (array) $link['remove']['variables'] as $var => $val )
				{
					$button_link .= URLEscape( '&' . $var . '=' . issetVal( $item[$val], '' ) );
				}

				echo '<td>' . button(
					'remove',
					$button_title,
					'"' . $button_link . '"'
				) . '</td>';
			}

			$color = issetVal( $item['row_color'] );

			if ( $cols )
			{
				foreach ( (array) $column_names as $key => $value )
				{
					echo $color === Preferences( 'HIGHLIGHT' ) ?
						'<td class="highlight">' :
						'<td>';

					if ( empty( $link[$key] ) || $item[$key] === false || isset( $_REQUEST['_ROSARIO_PDF'] ) )
					{
						echo issetVal( $item[$key], '&nbsp;' );

						echo '</td>';

						continue;
					}

					$link_url = $link[$key]['link'];

					foreach ( (array) $link[$key]['variables'] as $var => $val )
					{
						$link_url .= '&' . $var . '=' . $item[$val];
					}

					$link_url = URLEscape( $link_url );

					if ( ! empty( $link[$key]['js'] ) )
					{
						echo '<a href="#" onclick="' . AttrEscape( 'popups.open(' .
							json_encode( $link_url ) .
							'); return false;' ) . '"';
					}
					else
					{
						echo '<a href="' . $link_url . '"';
					}

					echo empty( $link[$key]['extra'] ) ? '' : ' ' . $link[$key]['extra'];

					echo '>';

					echo issetVal( $item[$key], '***' );

					echo '</a></td>';
				}
			}

			echo '</tr>';
		}

		if ( ! isset( $link['add']['first'] )
			|| ( $stop - $start + 1 ) < $link['add']['first'] )
		{
			if ( isset( $link['add']['link'] ) && ! isset( $_REQUEST['_ROSARIO_PDF'] ) )
			{
				echo '<tr><td colspan="' . ( $remove ? $cols + 1 : $cols ) . '">' .
				button(
					'add',
					issetVal( $link['add']['title'], '' ),
					( mb_strpos( $link['add']['link'], '"' ) === 0 ?
						$link['add']['link'] :
						'"' . URLEscape( $link['add']['link'] ) . '"' )
				) . '</td></tr>';
			}
			elseif ( isset( $link['add']['span'] ) && ! isset( $_REQUEST['_ROSARIO_PDF'] ) )
			{
				echo '<tr><td colspan="' . ( $remove ? $cols + 1 : $cols ) . '">' .
					button( 'add' ) . $link['add']['span'] . '</td></tr>';
			}
			elseif ( isset( $link['add']['html'] ) && $cols )
			{
				echo '<tr>';

				if ( $remove
					&& ! isset( $_REQUEST['_ROSARIO_PDF'] )
					&& ! empty( $link['add']['html']['remove'] ) )
				{
					echo '<td>' . $link['add']['html']['remove'] . '</td>';
				}
				elseif ( $remove && ! isset( $_REQUEST['_ROSARIO_PDF'] ) )
				{
					echo '<td>' . button( 'add' ) . '</td>';
				}

				foreach ( (array) $column_names as $key => $value )
				{
					echo '<td>' . issetVal( $link['add']['html'][$key], '' ) . '</td>';
				}

				echo '</tr>';
			}
		}

		echo '</tbody></table></div>';

		echo empty( $options['header'] ) ? '' : '</div>';
	}

	// END PRINT THE LIST ---.

	// NO RESULTS, BUT HAS ADD FIELDS ---.
	if ( $result_count == 0 )
	{
		if ( ! empty( $link['add']['link'] )
			&& ! isset( $_REQUEST['_ROSARIO_PDF'] ) )
		{
			echo '<div class="center">' .
			button(
				'add',
				issetVal( $link['add']['title'], '' ),
				( mb_strpos( $link['add']['link'], '"' ) === 0 ?
					$link['add']['link'] :
					'"' . URLEscape( $link['add']['link'] ) . '"' )
			) . '</div>';
		}
		elseif (  ( ! empty( $link['add']['html'] )
			|| ! empty( $link['add']['span'] ) )
			&& count( $column_names )
			&& ! isset( $_REQUEST['_ROSARIO_PDF'] ) )
		{
			if ( ! empty( $link['add']['html'] ) )
			{
				echo '<div class="list-wrapper"><table class="list widefat';

				echo $options['responsive'] ? ' rt' : '';

				echo $list_has_nav ? '' : ' list-no-nav';

				echo $options['center'] ? ' center' : '';

				echo '"><thead><tr>';

				echo '<th><span class="a11y-hidden">' . _( 'Delete' ) . '</span></th>';

				foreach ( (array) $column_names as $value )
				{
					echo '<th>' . str_replace( ' ', '&nbsp;', $value ) . '</th>';
				}

				echo '</tr></thead><tbody><tr><td>';

				echo ! empty( $link['add']['html']['remove'] ) ?
					$link['add']['html']['remove'] :
					button( 'add' );

				echo '</td>';

				foreach ( (array) $column_names as $key => $value )
				{
					echo '<td>' . issetVal( $link['add']['html'][$key], '' ) . '</td>';
				}

				echo '</tr></tbody></table></div>';
			}
			elseif ( ! empty( $link['add']['span'] ) )
			{
				echo '<table class="postbox';

				echo $options['center'] ? ' center' : '';

				echo '"><tr><td>' . button( 'add' ) . $link['add']['span'] . '</td></tr></table>';
			}
		}

		echo empty( $options['header'] ) ? '' : '</div>';
	}

	// END NO RESULTS, BUT HAS ADD FIELDS ---.

	echo '</div>'; // .list-outer.

	// List After hook.
	do_action( 'functions/ListOutput.fnc.php|list_after' );
}

/**
 * Reindex Results
 * Starting from 1
 *
 * Local function
 *
 * @example $result = _ReindexResults( $result );
 *
 * @param  array $array    Array to reindex
 * @return array Reindexed Array
 */
function _ReindexResults( $array )
{
	$new = [];

	$i = 1;

	foreach ( (array) $array as $value )
	{
		$new[$i] = $value;

		$i++;
	}

	return $new;
}

/*class Rosario_List implements Countable
{
	/**
	 * Get the count of elements in the container array.
	 *
	 * @link http://php.net/manual/en/countable.count.php
	 *
	 * @return int
	 */
	/*public function count()
	{
		return count( $this->container );
	}
}*/

/**
 * Search List
 *
 * Local function
 *
 * @example $result = _listSearch( $result, $LO_search );
 * @since 5.8
 *
 * @param  array  $result     ListOutput result.
 * @param  string $LO_search  ListOutput search term.
 * @return array  $result     Searched result.
 */
function _listSearch( $result, $LO_search )
{
	$result_count = count( $result );

	$search_term = trim( mb_strtolower( DBUnescapeString( $LO_search ) ) );

	$terms = [];

	if ( mb_substr( $search_term, 0, 1 ) != '"'
		|| mb_substr( $search_term, -1, 1 ) != '"' )
	{
		$search_term = str_replace( '"', '', $search_term );

		while ( $space_pos = mb_strpos( $search_term, ' ' ) )
		{
			$terms[mb_substr( $search_term, 0, $space_pos )] = 1;

			$search_term = mb_substr( $search_term, ( $space_pos + 1 ) );
		}

		$terms[trim( $search_term )] = 1;
	}
	elseif ( mb_strlen( $search_term ) > 2 )
	{
		// Search "expression".
		$search_term = str_replace( '"', '', $search_term );

		$terms[$search_term] = 1;
	}

	/* TRANSLATORS: List of words ignored during search operations */
	$ignored_words = explode( ', ', _( 'of, the, a, an, in' ) );

	foreach ( $ignored_words as $word )
	{
		unset( $terms[trim( $word )] );
	}

	foreach ( (array) $result as $key => $value )
	{
		$values[$key] = 0;

		foreach ( (array) $value as $val )
		{
			if ( empty( $val )
				&& $val !== '0' )
			{
				continue;
			}

			// FJ better list searching by isolating the values.
			$val = mb_strtolower( strip_tags( preg_replace( '/<script\b[^>]*>(.*?)<\/script>/is', "", $val ) ) );

			if ( $search_term == $val )
			{
				// +25 if Exact match.
				$values[$key] += 25;

				continue;
			}

			foreach ( $terms as $term => $one )
			{
				if ( mb_strpos( $val, $term ) !== false )
				{
					// +3 for each Term found.
					$values[$key] += 3;
				}
			}
		}

		if ( $values[$key] == 0 )
		{
			unset( $values[$key] );

			unset( $result[$key] );

			$result_count--;
		}
	}

	// Add Relevance column.
	if ( ! $result_count )
	{
		return $result;
	}

	array_multisort( $values, SORT_DESC, $result );

	$result = _ReindexResults( $result );

	$values = _ReindexResults( $values );

	$last_value = 1;

	$scale = ( 100 / $values[$last_value] );

	for ( $i = $last_value; $i <= $result_count; $i++ )
	{
		$score = (int) ( $values[$i] * $scale );

		$result[$i]['RELEVANCE'] = '<div class="bar relevance" style="width:' .
			$score . 'px;">' . $score . '</div>';
	}

	return $result;
}


/**
 * Save / Export List to CSV (OpenOffice), Tab (Excel) or XML
 *
 * Local function
 *
 * @example _listSave( $result, $column_names, Preferences( 'DELIMITER' ) );
 * @since 2.9
 * @since 5.8 Export list to Excel using MicrosoftXML (more reliable).
 *
 * @param  array  $result       ListOutput $result
 * @param  array  $column_names ListOutput $column_names
 * @param  string $singular     ListOutput $singular
 * @param  string $plural       ListOutput $plural
 * @param  string $delimiter    CSV|Tab|XML
 * @return void   Outputs file and exits
 */
function _listSave( $result, $column_names, $singular, $plural, $delimiter )
{
	$format_value =
	function ( $value )
	{
		$value = trim( preg_replace(
			'/ +/', // Remove double spaces.
			' ',
			str_replace(
				[ "\r", "\n", "\t", '[br][br]' ], // Convert new lines to [br], remove tabs.
				[ '', '[br]', '', '[br]' ],
				html_entity_decode(  // Decode HTML entities.
					strip_tags(  // Remove HTML tags.
						str_ireplace(
							[ '&nbsp;', '<br />' ], // Convert &nbsp; to space, <br /> to [br].
							[ ' ', '[br]' ],
							$value
						)
					),
					ENT_QUOTES
				) ) ) );

		// Remove first [br] if any.
		return mb_strpos( $value, '[br]' ) === 0 ? mb_substr( $value, 4 ) : $value;
	};

	switch ( $delimiter )
	{
		case 'CSV':
			$extension = 'csv';
			$delimiter = ',';

			break;

		case 'XML':
			$extension = 'xml';
			$delimiter = "";

			break;

		default: // Tab.

			$extension = 'xls';
			$delimiter = "\t";

			break;
	}

	// Clear output.
	ob_end_clean();

	$formatted_columns = $formatted_result = [];

	// Format Columns.
	foreach ( (array) $column_names as $column )
	{
		if ( $column !== '' )
		{
			$column = ParseMLField( $column );

			$column = $format_value( $column );

			$column = str_replace( '[br]', ' ', $column );
		}

		if ( $extension === 'csv' )
		{
			$column = '"' . str_replace( '"', '""', $column ) . '"';
		}

		$formatted_columns[] = $column;
	}

	$i = $extension === 'xls' ? 1 : 0;

	// Format Results.
	foreach ( (array) $result as $item )
	{
		$formatted_result[$i] = [];

		foreach ( (array) $column_names as $key => $value )
		{
			$value = issetVal( $item[$key], '' );

			if ( $value !== '' )
			{
				$value = preg_replace( '!<select.*selected\>([^<]+)<.*</select\>!i', '\\1', $value );

				$value = preg_replace( '!<select.*</select\>!i', '', $value );

				$value = $format_value( $value );

				$replace_br = $extension === 'xml' ? '[br]' : ' ';

				$value = str_replace( '[br]', $replace_br, $value );
			}

			if ( $extension === 'csv' )
			{
				$value = '"' . str_replace( '"', '""', $value ) . '"';
			}

			$formatted_result[$i][] = $value;
		}

		$i++;
	}

	// Generate output.
	if ( $extension === 'xls' )
	{
		/**
		 * Export list to Excel using MicrosoftXML (more reliable).
		 *
		 * @uses php-excel class.
		 *
		 * @since 5.8
		 *
		 * @link https://github.com/oliverschwarz/php-excel
		 */
		require_once 'classes/ExcelXML.php';

		$excel_xml = new Excel_XML;

		$formatted_rows = array_merge( [ $formatted_columns ], $formatted_result );

		$excel_xml->addWorksheet( ProgramTitle(), $formatted_rows );

		$excel_xml->sendWorkbook( ProgramTitle() . '.xls' );

		exit();
	}
	elseif ( $extension === 'csv' )
	{
		// 1st line: Columns.
		$output = implode( $delimiter, $formatted_columns );

		$output .= "\n";

		// Then values.
		foreach ( $formatted_result as $result_line )
		{
			$output .= implode( $delimiter, $result_line );

			$output .= "\n";
		}
	}

	// XML.
	else
	{
		$sanitize_xml_tag = function ( $name )
		{
			// Remove punctuation excepted underscores, points and dashes.
			$name = preg_replace( "/(?![.\-_])\p{P}/u", '', $name );

			// Lowercase and replace spaces by underscores.
			$name = mb_strtolower( str_replace( ' ', '_', $name ) );

			if ( (string) (int) mb_substr( $name, 0, 1 ) === mb_substr( $name, 0, 1 ) )
			{
				// Name cannot start with a number.
				$name = '_' . $name;
			}

			return $name;
		};

		$elements = 'items_set';

		$element = 'item';

		if ( $plural !== '.' )
		{
			// Sanitize XML tag names.
			$elements = $sanitize_xml_tag( $plural );

			$element = $sanitize_xml_tag( $singular );
		}

		$output = '<?xml version="1.0" encoding="UTF-8"?>' . "\n" . '<' . $elements . '>' . "\n";

		foreach ( $formatted_result as $result_line )
		{
			$output .= "\t" . '<' . $element . '>' . "\n";

			foreach ( $result_line as $key => $value )
			{
				if ( $formatted_columns[$key] === '' )
				{
					$column = 'column_' . ( $key + 1 );
				}
				else
				{
					// Sanitize XML tag names.
					$column = $sanitize_xml_tag( $formatted_columns[$key] );
				}

				// http://stackoverflow.com/questions/1091945/what-characters-do-i-need-to-escape-in-xml-documents
				$value = str_replace( '[br]', '<br />', AttrEscape( $value ) );

				$output .= "\t\t" . '<' . $column . '>' . $value .
					'</' . $column . '>' . "\n";
			}

			$output .= "\t" . '</' . $element . '>' . "\n";
		}

		$output .= '</' . $elements . '>';
	}

	// Download file
	header( "Cache-Control: public" );
	header( "Content-Type: application/" . $extension );
	header( "Content-Length: " . strlen( $output ) );
	header( "Content-Disposition: inline; filename=\"" . ProgramTitle() . "." . $extension . "\"\n" );

	echo $output;

	exit();
}
