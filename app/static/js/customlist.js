var options = {
  valueNames: [ 'name',
  'category',
  'price',
  'ambiance',
  'food',
  'tried',
  'commentary',
  'vegangluten',
  'loyalty',
  'chain',
  'location'
  ]
};

var fatassList = new List('fatass', options);

function filterVegan( isVegan ) {
  fatassList.filter(function(item) {
    return (item.values().vegangluten.indexOf(isVegan) >= 0);
  });
};

function filterLoyalty( isLoyalty ) {
  fatassList.filter(function(item) {
    return (item.values().loyalty.indexOf(isLoyalty) >= 0);
  });
}

function filterChain( isChain ) {
  fatassList.filter(function(item) {
    return (item.values().chain.indexOf(isChain) >= 0);
  });
}

function filterLocation( loc ) {
  fatassList.filter();
  fatassList.filter(function(item) {
    console.log(loc);
    return (item.values().location === loc);
  });
}
