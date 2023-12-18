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

    $('.countries_select').change(update_settlements_select)

    function get_comforts() {
        const comforts_list = document.querySelectorAll('#comforts_list input')

        let comforts = []

        comforts_list.forEach(comfort => {
            comforts.push({id: comfort.dataset.id,
                           value: comfort.value})
        })

        return comforts
    }

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

    $('#hide_street_button').click(function(e){
        if ($('.streets_select').attr('disabled') == 'disabled') {
            $('.streets_select').removeAttr('disabled')
            $('#hide_street_button').html('Не указывать улицу')
        } else {
            $('.streets_select').attr('disabled', true)
            $('#hide_street_button').html('Указать улицу')
        }
    })

    function getSelectValues(select) {
        var result = [];
        var options = select && select.options;
        var opt;

        for (var i=0, iLen=options.length; i<iLen; i++) {
            opt = options[i];

            if (opt.selected) {
                result.push(opt.value || opt.text);
            }
        }
        return result;
    }

    $('#search_form').submit(function(e){
        e.preventDefault()

        const housings_types = getSelectValues(document.querySelector('.housings_types_select'))
        const comforts = get_comforts()

        let street_id = null;

        if($('.streets_select').attr('disabled') != 'disabled') {
            street_id = $('.streets_select').val()
        }

        $.ajax({
            url: '/get_search_results',
            method: 'GET',
            data: {
                housings_types: JSON.stringify(housings_types),
                settlement_id: $('.settlements_select').val(),
                street_id: street_id,
                min_price: $('#min_price').val(),
                max_price: $('#max_price').val(),
                comforts: comforts,
                comforts_amount: comforts.length,
                date_start: $('#date_start').val(),
                date_end: $('#date_end').val()
            },
            success: function(records) {
                console.log(records)

                const recordsContainer = document.querySelector('.records_container')

                recordsContainer.innerHTML = ''

                records.forEach(record => {
                    recordsContainer.innerHTML += `<div class="column">
                    <div class="i_contain" onclick="window.location.href='/view_record?record_id=${record.id}'">
                    <div class="i_cards">
                        <img class="icon_logo" src="/static/images/${record.icon}"/>
                        <h2 class="i_title">${record.title}</h2>
                        <p class="i_summary">${record.description}</p>
                        <p class="i_summary">Цена: ${ record.price } рублей</p>
                        <p class="i_summary">Улица: ${ record.street_name }</p>
                        <p class="i_summary">Номер дома: ${record.house_number} </p>
                        <p class="i_summary">Номер квартиры: ${record.department_number ? record.department_number : 'Нет'}
                        <p class="i_summary">Пользователь: ${record.username}</p>
                        <p class="i_summary">Создано: ${record.created_data}</p>
                        <p class="i_summary">Последнее обновление: ${record.updated_time}</p>
                    </div>
                    </div>`
                })
            }
        })
    })

})