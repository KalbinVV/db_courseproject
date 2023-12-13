window.onload = function() {
    $.ajax({
        url: "/users/me",
        success: function(response) {
            parsed_response = JSON.parse(response)

            if(!parsed_response.is_quest) {
                $('.only_for_quest').hide(2)
                $('.only_for_authed').show(2)
            }
        }
    })

    $.ajax({
        url: "/housings_statistics",
        success: function(response) {
            const container = document.querySelector('.list-topics-content ul')

            const parsed_response = JSON.parse(response)

            console.log(parsed_response)

            for (key in parsed_response) {
                const innerElement = `<li>
							<div class="single-list-topics-content">
								<div class="single-list-topics-icon">
									<i class="flaticon-restaurant"></i>
								</div>
								<h2><a href="#">${key}</a></h2>
								<p>${parsed_response[key].count}</p>
								<p>${parsed_response[key].description}</p>
							</div>
						</li>`
				container.innerHTML += innerElement
            }
        }
    })
}