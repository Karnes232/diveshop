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