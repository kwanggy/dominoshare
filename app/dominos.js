function crawlMenu() {
    var pis = []
    $('.product').each(function(i) {
        var p = $(this);
        pis[i] = {
            name: p.find('.dominosColor1').text(),
            link: p.find('a.btn').attr('href'),
            img: p.find('img').attr('src'),
            desc: p.find('.description').text()
        };
    });
    console.log(pis);
    return pis;
}

function crawlDetails(pis) {
    var pds = [];
    var me = { pis: pis, pds: pds };
    $.proxy(__crawlDetails, me)(0);
}

function __crawlDetails(i) {
    var opts = [];
    var pis = this.pis;
    var pds = this.pds;
    console.log(pis);
    console.log('start ' + i);
    if(i >= pis.length) return;
    var p = pis[i];
    console.log(p.link);
    location.href = p.link;
    window.setTimeout(function() {
        $('label.row').each(function(j) {
            var row =  $(this);
            var tds = row.find('.td');
            opts[j] = {
                name: $(tds[0]).text(),
                price: $(tds[2]).text()
            };
        });

        p['options'] = opts;
        pds[i] = p;
        console.log((i+1)+'/'+pds.length);
        console.log(pds);
        var me = { pis: pis, pds: pds };
        $.proxy(__crawlDetails, me)(i+1);
    }, 2000);
}

var pis = [{"name":"Pizza","link":"/en/pages/order/#/product/S_PIZZA/builder/"},{"name":"Build Your Own Pasta","link":"/en/pages/order/#/product/S_BUILD/builder/"},{"name":"Boneless Chicken","link":"/en/pages/order/#/product/S_BONELESS/builder/"},{"name":"Wings","link":"/en/pages/order/#/product/S_BONEIN/builder/"},{"name":"Chicken & Bacon Carbonara","link":"/en/pages/order/#/product/S_PIZCT/builder/"},{"name":"Spinach & Feta","link":"/en/pages/order/#/product/S_PIZSE/builder/"},{"name":"Tuscan Salami & Roasted Veggie","link":"/en/pages/order/#/product/S_PIZSV/builder/"},{"name":"Italian Sausage & Pepper Trio","link":"/en/pages/order/#/product/S_PIZPT/builder/"},{"name":"Wisconsin 6 Cheese Pizza","link":"/en/pages/order/#/product/S_PIZCZ/builder/"},{"name":"Honolulu Hawaiian Pizza","link":"/en/pages/order/#/product/S_PIZUH/builder/"},{"name":"Philly Cheese Steak Pizza","link":"/en/pages/order/#/product/S_PIZPH/builder/"},{"name":"Pacific Veggie Pizza","link":"/en/pages/order/#/product/S_PIZPV/builder/"},{"name":"Cali Chicken Bacon Ranch™ Pizza","link":"/en/pages/order/#/product/S_PIZCR/builder/"},{"name":"Fiery Hawaiian™ Pizza","link":"/en/pages/order/#/product/S_PIZSU/builder/"},{"name":"Buffalo Chicken Pizza","link":"/en/pages/order/#/product/S_PIZBP/builder/"},{"name":"Memphis BBQ Chicken Pizza","link":"/en/pages/order/#/product/S_PIZCK/builder/"},{"name":"America's Favorite Feast®","link":"/en/pages/order/#/product/S_AX/builder/"},{"name":"Bacon Cheeseburger Feast®","link":"/en/pages/order/#/product/S_BX/builder/"},{"name":"Deluxe Feast®","link":"/en/pages/order/#/product/S_DX/builder/"},{"name":"ExtravaganZZa Feast®","link":"/en/pages/order/#/product/S_ZZ/builder/"},{"name":"MeatZZa Feast®","link":"/en/pages/order/#/product/S_MX/builder/"},{"name":"Ultimate Pepperoni Feast™","link":"/en/pages/order/#/product/S_PIZPX/builder/"},{"name":"Italian Sausage & Peppers","link":"/en/pages/order/#/product/S_SAUP/builder/"},{"name":"Buffalo Chicken","link":"/en/pages/order/#/product/S_BUFC/builder/"},{"name":"Chicken Habanero","link":"/en/pages/order/#/product/S_CHHB/builder/"},{"name":"Mediterranean Veggie","link":"/en/pages/order/#/product/S_MEDV/builder/"},{"name":"Philly Cheese Steak","link":"/en/pages/order/#/product/S_PHIL/builder/"},{"name":"Chicken Bacon Ranch","link":"/en/pages/order/#/product/S_CHIKK/builder/"},{"name":"Italian","link":"/en/pages/order/#/product/S_ITAL/builder/"},{"name":"Chicken Parm","link":"/en/pages/order/#/product/S_CHIKP/builder/"},{"name":"Chicken Alfredo","link":"/en/pages/order/#/product/S_ALFR/builder/"},{"name":"Italian Sausage Marinara","link":"/en/pages/order/#/product/S_MARIN/builder/"},{"name":"Chicken Carbonara","link":"/en/pages/order/#/product/S_CARB/builder/"},{"name":"Pasta Primavera","link":"/en/pages/order/#/product/S_PRIM/builder/"},{"name":"Build Your Own Pasta","link":"/en/pages/order/#/product/S_BUILD/builder/"},{"name":"Boneless Chicken","link":"/en/pages/order/#/product/S_BONELESS/builder/"},{"name":"Wings","link":"/en/pages/order/#/product/S_BONEIN/builder/"},{"name":"Stuffed Cheesy Bread","link":"/en/pages/order/#/product/F_SCBRD/builder/"},{"name":"Stuffed Cheesy Bread with Spinach & Feta","link":"/en/pages/order/#/product/F_SSBRD/builder/"},{"name":"Stuffed Cheesy Bread with Bacon & Jalapeno","link":"/en/pages/order/#/product/F_SBBRD/builder/"},{"name":"Parmesan Bread Bites","link":"/en/pages/order/#/product/F_PBITES/builder/"},{"name":"Breadsticks","link":"/en/pages/order/#/product/F_TWISTBRD/builder/"},{"name":"LAY'S® Classic Potato Chips","link":"/en/pages/order/#/product/F_LAYS/builder/"},{"name":"DORITOS® Nacho Cheese Tortilla Chips","link":"/en/pages/order/#/product/F_DORIT/builder/"},{"name":"Coke®","link":"/en/pages/order/#/product/F_COKE/builder/"},{"name":"Diet Coke®","link":"/en/pages/order/#/product/F_DIET/builder/"},{"name":"Sprite","link":"/en/pages/order/#/product/F_SPRITE/builder/"},{"name":"Dasani® Bottle Water","link":"/en/pages/order/#/product/F_WATER/builder/"},{"name":"Orange","link":"/en/pages/order/#/product/F_ORAN/builder/"},{"name":"Cinna Stix®","link":"/en/pages/order/#/product/F_CINBRD/builder/"},{"name":"Chocolate Lava Crunch Cake","link":"/en/pages/order/#/product/F_LAVA/builder/"},{"name":"Kicker Hot Sauce","link":"/en/pages/order/#/product/F_HOTCUP/builder/"},{"name":"Sweet Mango Habanero Sauce","link":"/en/pages/order/#/product/F_SMHAB/builder/"},{"name":"BBQ Sauce","link":"/en/pages/order/#/product/F_BBQC/builder/"},{"name":"Ranch","link":"/en/pages/order/#/product/F_SIDRAN/builder/"},{"name":"Blue Cheese","link":"/en/pages/order/#/product/F_Bd/builder/"},{"name":"Garlic Dipping Sauce","link":"/en/pages/order/#/product/F_SIDGAR/builder/"},{"name":"Icing Dipping Sauce","link":"/en/pages/order/#/product/F_SIDICE/builder/"},{"name":"Marinara Dipping Sauce","link":"/en/pages/order/#/product/F_SIDMAR/builder/"}];

function run() {
    pis.remove(0);
    pis.remove(0);
    crawlDetails(pis);
}
