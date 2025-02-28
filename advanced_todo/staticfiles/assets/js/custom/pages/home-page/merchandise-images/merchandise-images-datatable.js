
//MULTIPLE IMAGE UPLOADING WITH ORDERING

function imageUrlToBase64(url) {
    return new Promise(function (resolve, reject) {
        let img = new Image();
        img.crossOrigin = 'Anonymous';

        img.onload = function () {
            let canvas = document.createElement('canvas');
            let ctx = canvas.getContext('2d');
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0);

            // Get the base64 data URL from the canvas
            let dataURL = canvas.toDataURL('image/png');

            // Resolve the promise with the base64 data URL
            resolve(dataURL);
        };

        img.onerror = function () {
            // Reject the promise if there is an error loading the image
            reject(new Error('Failed to load image.'));
        };

        img.src = url;
    });
}
// Function to add an image to the sortable list
function addImageToSortable(order, id, imageUrl,index) {
    console.log('starteddd')
    $('#sortable').prepend('<li class="ui-state-default" data-order="' + order + '" data-id="' + id + '">' +
        '<div class="image-container">' +
        '<img src="' + imageUrl + '" style="width:100%;" /> ' +
        '<button class="delete-button" data-id="'+ id +'"" onclick="deleteImageCard(this)"><i class="fa fa-times del"></i></button>' +
        '</div>' +
        '<div class="order-number">' + index + '</div>' +
        '</li>');
}
function initialLoadImages (){
    let inputs = $('.initial-image input');
    let totalLength = inputs.length;

    $('.initial-image input').each(function (index) {
        let order = $(this).attr('data-order-id');
        let url = $(this).attr('data-url');
        let id = $(this).attr('data-id');
        let b_url = null
        
        // imageUrlToBase64(url)
        //     .then(function (base64Image) {
        //         // 'base64Image' contains the base64-encoded image data
        //         b_url = base64Image;
        //         // Now you can continue with your code here
        //     })
        //     .catch(function (error) {
        //         console.error('Error:', error);
        //     });
        // Create an object to store the data
        addImageToSortable(order,id,url,totalLength)
        totalLength-=1
        let imageData = {
            order: order,
            url: url,
            id: id
        };

        // Push the object to the array
    });
}
initialLoadImages()
console.log('completed')

$(function () {
    $('#images').change(function (e) {
        // Show the loading overlay
        $('#loading-overlay').show();
    
        let files = e.target.files;
        let formData = new FormData();
        let order = 1
        for (let file of files){
            formData.append(order++,file)
        }
    
        // Add the CSRF token to the FormData
        formData.append('csrfmiddlewaretoken', api_config['csrfmiddlewaretoken']);
    
        $.ajax({
            url: api_config['image-order'],
            method: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                console.log(response);
    
                // Check if the response status is 200 and the message is 'Success'
                if (response.status_code === 200 && response.message === 'Success') {
                    // Get the URL to redirect to from the data-href attribute of the button
                    let redirectUrl = $('#save-button').data('href');
    
                    // Hide the loading overlay before redirecting
                    $('#loading-overlay').hide();
    
                    // Redirect to the specified URL
                    window.location.href = redirectUrl;
                }
            },
            error: function (error) {
                console.error(error);
                // Hide the loading overlay in case of an error
                $('#loading-overlay').hide();
            }
        });
    });
    
    
    
    $('#sortable').sortable();
    $('#sortable').disableSelection();

    // Sortable events
    $('#sortable').on('sortbeforestop', function (event) {
        reorderImages();
    });

    function reorderImages() {
        // Get the items
        
        let images = $('#sortable li');
        let i = 0, nrOrder = 0;
        
        for (i; i < images.length; i++) {
            let image = $(images[i]);
            if (image.hasClass('ui-state-default') && !image.hasClass('ui-sortable-placeholder')) {
                image.attr('data-order', nrOrder);
                let orderNumberBox = image.find('.order-number');
                orderNumberBox.html(nrOrder + 1);
                nrOrder++;
            }
        }

        // Collect image data and send it via AJAX
        let imageArray = [];
        images.each(function (index) {
            let image = $(this);
            if(!image.hasClass('ui-sortable-placeholder')){
                
            
                let order = index+=1;
                let imageId = image.data('id');
                imageArray.push({
                    order: order,
                    image_id: imageId,
                });
            }
        });
        // Send the image data via AJAX
        $.ajax({
            url: api_config['image-order'],
            method: 'POST',
            data: {
                images: JSON.stringify(imageArray),
                csrfmiddlewaretoken: api_config['csrfmiddlewaretoken'],
                is_update: 'True',
            },
            success: function (response) {
                console.log(response);
            },
            error: function (error) {
                console.error(error);
            }
        });
    }
});

function deleteImageCard(a) {
    let instanceId = $(a).data('id');
    $.ajax({
        url: api_config['delete-image'],
        method: 'POST',
        data: {
            instance_id: instanceId,
            csrfmiddlewaretoken: api_config['csrfmiddlewaretoken'],
        },
        success: function (response) {
            console.log(response);
            location.reload();
        },
        error: function (error) {
            console.error(error);
        }
    });
}



$('#save-button').click(function () {
    // Get the URL to redirect to from the data-href attribute of the button
    let redirectUrl = $(this).data('href');
    
    // Redirect to the specified URL
    window.location.href = redirectUrl;
});



// DELETE ALL API CALL ON CLICK
$(document).ready(function() {
    $('.btn-remove').click(function() {
        // Show a confirmation dialog
        Swal.fire({
            title: 'Confirm Delete',
            text: 'Are you sure you want to remove all images?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Yes, remove all',
            cancelButtonText: 'No, cancel',
        }).then((result) => {
            if (result.isConfirmed) {
                // User clicked "Yes, remove all," so execute the AJAX request
                let is_delete_all = true; // Set to true or false as needed

                $.ajax({
                    url: api_config['delete-image'],
                    method: 'POST',
                    data: {
                        is_delete_all: is_delete_all,
                        csrfmiddlewaretoken: api_config['csrfmiddlewaretoken'],
                    },
                    success: function (response) {
                        Swal.fire('Deleted', 'All images have been removed.', 'success');
                        
                        // Reload the page after a successful delete
                        setTimeout(function() {
                            location.reload();
                        }, 1000);
                    },
                    error: function (error) {
                        Swal.fire('Error', 'An error occurred while removing images.', 'error');
                    }
                });
            }
        });
    });
});
