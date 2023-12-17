$(document).ready(function(){
    $('#add_record_form').submit(function(e){
        e.preventDefault()

        $.ajax({
            method: "POST",
            url: "/create_record",
            data: {
                housing_id: $("#housing_id").val(),
                title: $('#title').val(),
                description: $('#description').val(),
                price: $('#price').val(),
            },
            success: function(response) {
                window.location.href = '/view_record?record_id='+response
            },
            error: function(response) {
                console.log(response)
            }
        })
    })
})