// Function to show an element
function showElement(element) {
    if (element) {
        element.style.display = 'block'; // Change display property to 'block'
    }
}

// Function to hide an element
function hideElement(element) {
    if (element) {
        element.style.display = 'none'; // Change display property to 'none'
    }
}



"use strict";

// Class definition
const MCUpdateOrCreateProperty = function () {

    let validator;
    let file_type_element;
    let form;
    const handleSubmit = () => {
        // Get elements
        form = document.getElementById('create-or-update-company-profile-form');
        const submitButton = document.getElementById('create-or-update-company-profile-submit');
        validator = FormValidation.formValidation(
            
            form,
            {
                fields: {
                    'title': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
         
                    'description_title': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
          
                    'meta_title': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    'meta_keyword': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    'meta_image_title': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    'meta_description': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    
                    'service_image': {
                        validators: {
                            file: {
                                maxSize: 1024 * 1024, // Maximum file size in bytes (1 MB)
                                message: 'The selected file is not valid or is above 1 MB'
                            },
                           
                        }
                    },
                    'logo_image': {
                        validators: {
                            file: {
                                maxSize: 1024 * 1024, // Maximum file size in bytes (1 MB)
                                message: 'The selected file is not valid or is above 1 MB'
                            },
                           
                        }
                    },
                    'og_image': {
                        validators: {
                            file: {
                                extension: 'jpg,jpeg,png',
                                type: 'image/jpeg,image/png',
                                maxSize: 1024 * 1024, // Maximum file size in bytes (1 MB)
                                message: 'The selected file is not valid or is above 1 MB'
                            },
                           
                        }
                    },
                    
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger(),
                    bootstrap: new FormValidation.plugins.Bootstrap5({
                        rowSelector: '.fv-row',
                        eleInvalidClass: '',
                        eleValidClass: ''
                    })
                }
            }
        );
        
        submitButton.addEventListener('click', async e => {
            e.preventDefault();
            let selectElement = document.getElementById('file-type-select');
            var selectedValue = selectElement.value;
            var selectedValue = selectElement.value;

                if (selectedValue === 'video') {
                    validator.addField('url', {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    });
                }
            if (validator) {
                const status = await validator.validate();
                console.log('validated!');
        
                if (status === 'Valid') {
                    submitButton.setAttribute('data-kt-indicator', 'on');
                    submitButton.disabled = true;
        
                    try {
                        const formData = new FormData();
                        formData.append('instance_id', document.querySelector('[name="instance_id"]').value);
                        formData.append('title', document.querySelector('[name="title"]').value);
                        formData.append('url', document.querySelector('[name="url"]').value);
                        formData.append('full_name', document.querySelector('[name="full_name"]').value);
                        formData.append('order', document.querySelector('[name="order"]').value);
                        formData.append('description_title', document.querySelector('[name="description_title"]').value);
                        // formData.append('description', document.querySelector('[name="description"]').value);
                        formData.append('description', CKEDITOR.instances.mytextarea.getData());
                        formData.append('work_uuid', document.querySelector('[name="work_uuid"]').value);
                        formData.append('service_image', document.querySelector('[name="service_image"]').files[0]);
                        formData.append('logo_image', document.querySelector('[name="logo_image"]').files[0]);
                        formData.append('file_type', document.querySelector('[name="file_type"]').value);
                        
                        // SEO
                        formData.append('meta_title', document.querySelector('[name="meta_title"]').value);
                        formData.append('meta_description', document.querySelector('[name="meta_description"]').value);
                        formData.append('meta_keyword', document.querySelector('[name="meta_keyword"]').value);
                        formData.append('meta_image_title', document.querySelector('[name="meta_image_title"]').value);
                        formData.append('og_image', document.querySelector('[name="og_image"]').files[0]);
        
                        const btn = document.getElementById('create-or-update-company-profile-submit');
                        const loadingBtn = document.getElementById('banner-loader-text');
        
                        btn.style.display = 'none';
                        loadingBtn.style.display = 'inline-block';
        
                        const response = await fetch(api_config.create_or_update_from, {
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': api_config.csrfmiddlewaretoken,
                            },
                            body: formData,
                        });
        
                        const data = await response.json();
        
                        if (response.ok) {
                            const redirectUrl = form.getAttribute('data-redirect-url');
                            if (redirectUrl) {
                                location.href = redirectUrl;
                            }
                        } else {
                            submitButton.removeAttribute('data-kt-indicator');
                            btn.style.display = 'inline-block';
                            loadingBtn.style.display = 'none';
                            submitButton.disabled = false;
        
                            Swal.fire({
                                html: data.message || "Please try again.",
                                icon: "error",
                                buttonsStyling: false,
                                confirmButtonText: "Ok, got it!",
                                customClass: {
                                    confirmButton: "btn btn-primary"
                                }
                            });
                        }
                    } catch (error) {
                        console.error('Error during submission:', error);
                        submitButton.removeAttribute('data-kt-indicator');
                        submitButton.disabled = false;
        
                        Swal.fire({
                            html: "An error occurred. Please try again.",
                            icon: "error",
                            buttonsStyling: false,
                            confirmButtonText: "Ok, got it!",
                            customClass: {
                                confirmButton: "btn btn-primary"
                            }
                        });
                    }
                } else {
                    submitButton.removeAttribute('data-kt-indicator');
                    submitButton.disabled = false;
        
                    Swal.fire({
                        html: "Sorry, looks like there are some errors detected. Please try again.",
                        icon: "error",
                        buttonsStyling: false,
                        confirmButtonText: "Ok, got it!",
                        customClass: {
                            confirmButton: "btn btn-primary"
                        }
                    });
                }
            }
        });
        

    }



    const handleDropzone = () => {

        let dropZone_is=false
        let ProductImageDropzone = new Dropzone("#campaign_images_dropzone", {
            url: `${api_config.campaign_image_upload_api_url}`,
            acceptedFiles: ".jpeg,.jpg,.png",
            maxFiles: 10,
            paramName: "file",
            maxFilesize: 1, // MB
            addRemoveLinks: true,
            accept: function(file, done) {
                done();
            },
            init: function() {

                this.on("maxfilesexceeded", function (data) {
                    let res = eval('(' + data.xhr.responseText + ')');
                });
                this.on("error", function (file, message) {
                Swal.fire({
                    html: "The uploaded file is invalid, please try again",
                    icon: "error",
                    buttonsStyling: false,
                    confirmButtonText: "Ok, got it!",
                    customClass: {
                        confirmButton: "btn btn-primary"
                    }
                });
                    this.removeFile(file);
                });
                this.on("sending", function(file, xhr, formData){
                    formData.append("uuid", `${api_config.uuid}`);
                    formData.append("csrfmiddlewaretoken", `${api_config.csrfmiddlewaretoken}`);
                    formData.append("files", file);
                    formData.append("module", 'product-images');
                });
                this.on("success", function(file, responseText) {
                    if(responseText.status_code == 200 && (ProductImageDropzone.files.length > 0 || $("#campaign_images_dropzone").find('img').length))
                    {
                        dropZone_is=true;
                        //element = file.previewElement.getElementsByTagName('a')?.[0];
                        //element.setAttribute('instance_id', responseText.data);
                        let childElements = file?.previewElement?.children;
                        childElements.forEach(childElement => {
                            childElement.setAttribute('instance_id', responseText.data);
                            childElement.setAttribute('action_type', 5);
                        });
                    }
                });
                this.on('removedfile', function(file) {
                    let removeElement = file.previewElement.getElementsByTagName('a')?.[0];
                    let instance_id = removeElement.getAttribute('instance_id')
                    let action_type = removeElement.getAttribute('action_type')
                    $.post(`${api_config.temporary_image_destroy_api_url}`, { id: instance_id, action_type:action_type }, 
                        function(data, status, xhr) {
                            if (ProductImageDropzone.files.length <= 0) {
                                dropZone_is = false
                                console.log("less than",data)
                            }
                        
                            console.log("greater than",data)

                        }).done(function() { console.log('Request done!'); })
                        .fail(function(jqxhr, settings, ex) { console.log('failed, ' + ex); });

                }); 
            }
        });



        ProductImageDropzone.on("addedfile", file => {
            let instance_id = file?.instance_id;
            let childElements = file?.previewElement?.children;
            childElements.forEach(childElement => {
                childElement.setAttribute('instance_id', instance_id);
                childElement.setAttribute('action_type', 5);
            });
        });
        

        $.post(`${api_config.get_campaign_images_api_url}`, { campaign_id: `${api_config.campaign_id}` }, 
            function(data, status, xhr) {
                if(data.status_code == 200)
                {
                    $.each(data.data, function (key,value) {
                        let mockFile = { name: value.image_name, size: value.size, instance_id: value.id};
                        ProductImageDropzone.emit("addedfile", mockFile);
                        generateBase64encodedURL(value.image, function(dataURL){ 
                            ProductImageDropzone.emit("thumbnail", mockFile, dataURL)
                        })
                        ProductImageDropzone.emit("complete", mockFile);
                    
                    });
                    
                }
                

            }
        ).done(function() { console.log('Request done!'); 
        }).fail(function(jqxhr, settings, ex) { console.log('failed, ' + ex); });
    }



    const handleInit = () => {

        const fileElementDiv        = document.querySelector('[data-id="file-element-div"]');
        const dropzoneElementDiv    = document.querySelector('[data-id="dropzone-element-div"]');


        
        file_type_element.addEventListener('change', function(e) {
            switch ($(this).val()) {
                case 'video':
                    showElement(fileElementDiv);  
                    hideElement(dropzoneElementDiv); 
                    break;
                case 'image':
                    showElement(dropzoneElementDiv);  
                    hideElement(fileElementDiv); 
                    break;
                default:
                    break;
            }

            console.log();

        });

    }

    
    // Public methods
    return {
        init: function () {

            file_type_element = document.querySelector('[id="file-type-select"]');

            handleInit();

            // Create a new 'change' event
            const event = new Event('change', {
                bubbles: true,
                cancelable: true
            });

            // Dispatch the event on the select element
            file_type_element.dispatchEvent(event);


            handleSubmit();
            handleDropzone();
            
        }
    };
}();




// On document ready
KTUtil.onDOMContentLoaded(function () {
    MCUpdateOrCreateProperty.init();
});





function previewImage(event) {
    let logoPreview = document.getElementById('logo-preview');
    logoPreview.src = URL.createObjectURL(event.target.files[0]);
    logoPreview.style.display = "block";
}




function logopreviewImage(event) {
    let logoPreview = document.getElementById('main-logo-preview');
    logoPreview.src = URL.createObjectURL(event.target.files[0]);
    logoPreview.style.display = "block";
}

function generateBase64encodedURL(src, callback){
    let image = new Image();
    image.crossOrigin = 'Anonymous';
    image.onload = function(){
        let canvas = document.createElement('canvas');
        let context = canvas.getContext('2d');
        //canvas.height = this.naturalHeight;
        canvas.height = 140;
        canvas.width = 140;
        //canvas.width = this.naturalWidth;
        context.drawImage(this, 0, 0,140,140);
        let dataURL = canvas.toDataURL('image/jpeg');
        callback(dataURL);
    };
    image.src = src;
}

function ogimagepreviewImage(event) {
    let logoPreview = document.getElementById('og-image-logo-preview');
    logoPreview.src = URL.createObjectURL(event.target.files[0]);
    logoPreview.style.display = "block";
}


$('#features').repeater({
    initEmpty: false,
    defaultValues: false, // Set this to false to use the placeholders instead of default values

    show: function () {
        $(this).slideDown();
        $(this).find('input[name="name"]').attr('placeholder', 'Title');
        $(this).find('textarea[name="description"]').attr('placeholder', 'Description');
    },

    hide: function (deleteElement) {
        $(this).slideUp(deleteElement);
    }
});


