$(document).ready(function() {
    // Add CSRF token to all AJAX requests
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
        const scoreContainer = $(this).closest('.score-container').find('.album-score');
        
        $.ajax({
            url: '/rango/vote/',
            type: 'POST',
            data: {
                'album_id': albumId,
                'vote_type': voteType
            },
            success: function(response) {
                if (response.status === 'success') {
                    // Update the score display
                    scoreContainer.text(response.new_score);
                    
                    // Update classes based on score
                    scoreContainer.removeClass('positive negative');
                    if (response.new_score > 0) {
                        scoreContainer.addClass('positive');
                    } else if (response.new_score < 0) {
                        scoreContainer.addClass('negative');
                    }
                    
                    // Update button styles
                    const upvoteBtn = $(`.upvote-btn[data-album-id="${albumId}"]`);
                    const downvoteBtn = $(`.downvote-btn[data-album-id="${albumId}"]`);
                    
                    upvoteBtn.removeClass('active');
                    downvoteBtn.removeClass('active');
                    
                    if (response.action !== 'removed') {
                        if (voteType === 'up') {
                            upvoteBtn.addClass('active');
                        } else {
                            downvoteBtn.addClass('active');
                        }
                    }
                }
            }
        });
    });
});