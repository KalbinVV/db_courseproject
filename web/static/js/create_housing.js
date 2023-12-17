$(document).ready(function() {
    $('.countries_select').select2()
    $('.settlements_select').select2()

    $('.comfort_range').change(function(e){
        const current_target = e.currentTarget

        const span_value = document.querySelector('#value-'+current_target.id)

        span_value.innerHTML = current_target.value
    })

    $('.streets_select').select2({
        ajax: {
                url: '/api/get_streets_by_like_name',
                data: function (params) {
                    var query = {
                        search: params.term,
                        settlement_id: $('.settlements_select').val()
                    }

                    return query
                },
                processResults: function (data) {
                    console.log(data.items)
                    return {
                        results: data
                    };
                }
        }
    });

    $('.housings_types_select').select2()

    $('.housings_types_select').change(() => {
        update_department_number_visible()
        update_icon()
    })

    $('.countries_select').change(update_settlements_select)

    update_department_number_visible()
    update_icon()

    function get_comforts() {
        const comforts_list = document.querySelectorAll('#comforts_list input')

        let comforts = []

        comforts_list.forEach(comfort => {
            comforts.push({id: comfort.dataset.id,
                           value: comfort.value})
        })

        return comforts
    }

    $('#add_housing_form').submit(function(e){
        e.preventDefault()

        comforts = get_comforts()

        console.log(comforts)

        $.ajax({
            method: "POST",
            url: "/api/add_housing",
            data: {
                name: $('#name').val(),
                description: $('#description').val(),
                street_id: $('.streets_select').val(),
                house_number: $('#house_number').val(),
                department_number: $('#department_number').val(),
                housing_type_id: $('.housings_types_select').val(),
                comforts: comforts,
                comforts_amount: comforts.length
            },
            success: function(response) {
                if (response.successful){
                    window.location.href = '/view_housing?housing_id=' + response.housing_id
                } else {
                    alert('Не удалось создать объявление: ' + response.message)
                }
            },
            error: function(response) {
                console.log(response)
            }
        })
    })

    update_settlements_select()

    function update_settlements_select() {
        $.ajax({
            method: "GET",
            url: "/api/get_settlements_by_country",
            data: {
                country_id: $('.countries_select').val()
            },
            success: function(settlements_list) {
                const settlements_select = document.querySelector('.settlements_select');

                settlements_select.innerHTML = ''

                settlements_list.forEach(settlement => {
                    settlements_select.innerHTML += `<option value=${settlement.id}>
                        ${settlement.name}
                    </option>`
                })

            }
        })
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
})