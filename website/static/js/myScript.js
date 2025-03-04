// Increase Quantity (+ Button)
$(document).on('click', '.plus-cart', function(){
    console.log('Plus Button Clicked');

    var id = $(this).attr('pid').toString();
    var quantity = $(this).siblings('span');

    $.ajax({
        type: 'GET',
        url: '/pluscart',
        data: { cart_id: id },
        success: function(data) {
            console.log(data);
            quantity.text(data.quantity);
            $('#quantity' + id).text(data.quantity);
            $('#amount_tt').text(data.amount);
            $('#totalamount').text(data.total);
        }
    });
});

// Decrease Quantity (- Button)
$(document).on('click', '.minus-cart', function(){
    console.log('Minus Button Clicked');

    var id = $(this).attr('pid').toString();
    var quantity = $(this).siblings('span');

    $.ajax({
        type: 'GET',
        url: '/minuscart',
        data: { cart_id: id },
        success: function(data) {
            console.log(data);
            if (data.quantity <= 0) {
                location.reload(); // Reload page if quantity becomes zero
            } else {
                quantity.text(data.quantity);
                $('#quantity' + id).text(data.quantity);
                $('#amount_tt').text(data.amount);
                $('#totalamount').text(data.total);
            }
        }
    });
});

// Remove Item from Cart
$(document).on('click', '.remove-cart', function(){
    var id = $(this).attr('pid').toString();
    var to_remove = $(this).closest('.row');

    $.ajax({
        type: 'GET',
        url: '/removecart',
        data: { cart_id: id },
        success: function(data) {
            $('#amount_tt').text(data.amount);
            $('#totalamount').text(data.total);
            to_remove.remove();
        }
    });
});


$('.remove-cart').click(function(){
    
    var id = $(this).attr('pid').toString()

    //parentNode represents every div that is to be removed
    var to_remove = this.parentNode.parentNode.parentNode.parentNode

    $.ajax({
        type: 'GET',
        url: '/removecart',
        data: {
            cart_id: id
        },

        success: function(data){
            document.getElementById('amount_tt').innerText = data.amount
            document.getElementById('totalamount').innerText = data.total
            to_remove.remove()
        }
    })


})