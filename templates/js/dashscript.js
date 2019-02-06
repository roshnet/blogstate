//
// Function: UI
//

function ui() {
  
  function maxwidth768action(mql){
    
    var mql = window.matchMedia( 'screen and (max-width: 768px)' );
    
    if ( mql.matches ) {
      $('.dashboard-sidebar').addClass('dashboard-sidebar--mini');
    }
    else {
      $('.dashboard-sidebar').removeClass('dashboard-sidebar--mini');
    }
  }

  maxwidth768action(mql); // run on load
  mql.addListener(maxwidth768action); // run whenever media query is triggered

  console.log('UI loaded!');
  
}

//
// Function: List View (using List.js)
//

function listView() {
    
  var thisList = 'dashboard'; // Must be an id
    
  var options = {
    listClass: 'page-body',
    searchClass: 'search-field',
    //indexAsync: true,
    valueNames: [
      'list-item__title',
      'list-item__author',
      'list-item__review',
      'list-item__state',
      'list-item__date',
      'list-item__country'
    ],
    //item: '<div class="searchable-select__option"><div class="searchable-select__option__label"></div></div>'
  };
    
  //var values = searchableOptions;
    
  var list = new List(thisList, options);

  console.log('List View loaded!');

};



//
// Execute scripts when document is ready
//

$(document).ready(function() {
  ui();
  listView();
});