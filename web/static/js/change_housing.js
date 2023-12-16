$(document).ready(function() {
    update_department_number_visible()
    update_icon()

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