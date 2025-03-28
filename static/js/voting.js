$(document).ready(function() {
    // CSRF token function remains unchanged
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    const csrftoken = getCookie('csrftoken');
    
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Handle voting
    $('.vote-btn').click(function() {
        const albumId = $(this).data('album-id');
        const voteType = $(this).data('vote-type');
        // Use closest .vote-container (adjust if your markup differs) to find the album score display
        const scoreContainer = $(this).closest('.vote-container').find('.album-score');
        
        $.ajax({
            url: '/rango/vote/',
            type: 'POST',
            data: {
                'album_id': albumId,
                'vote_type': voteType
            },
            success: function(response) {
                if (response.status === 'success') {
                    // Update the score immediately on success
                    scoreContainer.text(response.new_score);
                    
                    // Remove active states from vote buttons in container
                    const voteContainer = $(scoreContainer).closest('.vote-container');
                    voteContainer.find('.vote-btn').removeClass('active');
                    
                    // Mark the clicked button as active if vote was applied
                    if (response.action !== 'removed') {
                        $(this).addClass('active');
                    }
                }
            },
            error: function(xhr, status, error) {
                console.error('AJAX Error:', error);
            }
        });
    });
});