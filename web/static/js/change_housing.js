$(document).ready(function() {
    update_department_number_visible()
    update_icon()

    $('.comfort_range').change(function(e){
        const current_target = e.currentTarget

        const span_value = document.querySelector('#value-'+current_target.id)

        span_value.innerHTML = current_target.value
    })

    update_comforts_range()

    function update_comforts_range() {
        const comforts_list = document.querySelectorAll('#comforts_list input')

        comforts_list.forEach(comfort => {
            const span_value = document.querySelector('#value-'+comfort.id)

            span_value.innerHTML = comfort.value
        })
    }

    function get_comforts() {
        const comforts_list = document.querySelectorAll('#comforts_list input')

        let comforts = []

        comforts_list.forEach(comfort => {
            comforts.push({id: comfort.dataset.id,
                           value: comfort.value})
        })

        return comforts
    }

    function update_department_number_visible() {
        const is_visible = $('.housings_types_select').find(':selected').attr('data-department_number_required')

        if (is_visible.toLowerCase() === 'true') {
            $('.department_number_container').show()
        } else {
            $('.department_number_container').hide()
        }
    }

    function update_icon() {
        const icon = $('.housings_types_select').find(':selected').attr('data-icon')

        $('.type_icon').attr('src', '/static/images/' + icon)
    }

    $('#change_housing_form').submit(function(e){
        e.preventDefault()

        comforts = get_comforts()

        console.log(comforts)

        $.ajax({
            method: "POST",
            url: "/change_housing",
            data: {
                housing_id: $("#housing_id").val(),
                name: $('#name').val(),
                description: $('#description').val(),
                comforts: comforts,
                comforts_amount: comforts.length
            },
            success: function(response) {
                window.location.href = '/view_housing?housing_id=' + response
            },
            error: function(response) {
                console.log(response)
            }
        })
    })
})