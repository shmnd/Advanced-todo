"use strict";

// Class definition
const MCSaveCategory = function () {
    const handleSubmit = () => {
        let validator;

        // Get elements
        const form = document.getElementById('create-or-update-campaigns-form');
        const submitButton = document.getElementById('create-or-update-campaigns-submit');

 

        validator = FormValidation.formValidation(
            
            form,
            {
                fields: {
                    'title': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            },
                        }
                    },
                    'web_link': {
                        validators: {
                            notEmpty: {
                                enabled: false,
                                message: 'This field is required',
                            },
                            uri: {
                                message: 'Please enter a valid URL'
                            }
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


        submitButton.addEventListener('click', e => {
            e.preventDefault();

            // Validate form before submit
            if (validator) {
                validator.validate().then(function (status) {
                    console.log('validated!');
                    submitButton.setAttribute('data-kt-indicator', 'on');

                    // Disable button to avoid multiple click
                    submitButton.disabled = true;

                    if (status == 'Valid') {

                        // Handle submit button
                        e.preventDefault();
                     const btn = document.getElementById('create-or-update-campaigns-submit');
                      const text = document.getElementById('banner-loader-text');
                      console.log('HERE');
                      // alert('HERE')
                      // debugger;
                      btn.disabled = true;
                      btn.style.display = 'none';
                      text.style.display = 'block';

                        submitButton.setAttribute('data-kt-indicator', 'on');

                        // Disable submit button whilst loading
                        submitButton.disabled = true;
                        submitButton.removeAttribute('data-kt-indicator');
                        // Enable submit button after loading
                        submitButton.disabled = false;

                        // Redirect to customers list page
                        form.submit();
                    } else {
                        submitButton.removeAttribute('data-kt-indicator');

                        // Enable button
                        submitButton.disabled = false;
                        Swal.fire({
                            html: "Sorry, looks like there are some errors detected, please try again.",
                            icon: "error",
                            buttonsStyling: false,
                            confirmButtonText: "Ok, got it!",
                            customClass: {
                                confirmButton: "btn btn-primary"
                            }
                        });
                    }
                });
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
                                // console.log(data)
                            }
                        
                            // console.log(data)

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




    
    // Public methods
    return {
        init: function () {
            handleSubmit();
            handleDropzone();
        }
    };
}();

// On document ready
KTUtil.onDOMContentLoaded(function () {
    MCSaveCategory.init();
});




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
