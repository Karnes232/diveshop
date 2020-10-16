document.addEventListener('DOMContentLoaded', function() {
    // Use buttons to toggle between views
  document.querySelector('#insertrow2').addEventListener('click', row2);
  document.querySelector('#insertrow3').addEventListener('click', row3);

})

function row2() {

    // Show compose view and hide other views
    document.querySelector('#insertrow2').style.display = 'none';
    document.querySelector('#row2').style.display = '';
    document.querySelector('#insertrow3').style.display = '';
}

function row3() {

    // Show compose view and hide other views
    document.querySelector('#insertrow3').style.display = 'none';
    document.querySelector('#row3').style.display = '';

}

function total_sale() {

    let quantity1 = parseInt( document.getElementById("quantity1").value );
    let quantity2 = parseInt( document.getElementById("quantity2").value );
    let quantity3 = parseInt( document.getElementById("quantity3").value );
    let price1 = parseInt( document.getElementById("price1").value );
    let price2 = parseInt( document.getElementById("price2").value );
    let price3 = parseInt( document.getElementById("price3").value );
    var result = (quantity1 * price1)+(quantity2 * price2)+(quantity3 * price3)
    return(`Total Cost is $${result}, Are you sure?`)
 
    

}

function confirm2() {
    confirm('Are you sure?');

}