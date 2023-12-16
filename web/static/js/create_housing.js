$(document).ready(function() {
    $('.countries_select').select2()
    $('.settlements_select').select2()

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

    $('.housings_types_select').change(update_department_number_visible)

    $('.countries_select').change(update_settlements_select)

    update_department_number_visible()

    $('#add_housing_form').submit(function(e){
        e.preventDefault()

        $.ajax({
            method: "POST",
            url: "/api/add_housing",
            data: {
                name: $('#name').val(),
                description: $('#description').val(),
                street_id: $('.streets_select').val(),
                house_number: $('#house_number').val(),
                department_number: $('#department_number').val(),
                housing_type_id: $('.housings_types_select').val()
            },
            success: function(response) {
                window.location.href = '/my_housings'
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
})