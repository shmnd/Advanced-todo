function previewImage(event) {
    let logoPreview = document.getElementById('logo-preview');
    logoPreview.src = URL.createObjectURL(event.target.files[0]);
    logoPreview.style.display = "block";
}

function ImagePreviewLogoImage(event) {
    let logoPreview = document.getElementById('project_logo_image_preview');
    logoPreview.src = URL.createObjectURL(event.target.files[0]);
    logoPreview.style.display = "block";
}

function BannerImagePreviewImage(event) {
    let logoPreview = document.getElementById('project_Banner_image_preview');
    logoPreview.src = URL.createObjectURL(event.target.files[0]);
    logoPreview.style.display = "block";
}

function ogimagepreviewImage(event) {
    let logoPreview = document.getElementById('og-image-logo-preview');
    logoPreview.src = URL.createObjectURL(event.target.files[0]);
    logoPreview.style.display = event.target.files.length > 0 ? 'block' : 'none';
}

// For Image Remove
function removeImage(inputId, previewId) {
    let logoInput = document.getElementById(inputId);
    let logoPreview = document.getElementById(previewId);
    logoInput.value = '';
    logoPreview.style.display = 'none';
    document.querySelector('.remove-button').remove();
}


    $('#features').repeater({
        initEmpty: false,
    
        defaultValues: {
            'text-input': 'foo'
        },
    
        show: function () {
            $(this).slideDown();
        },
    
        hide: function (deleteElement) {
            $(this).slideUp(deleteElement);
        }
    });
    
    $('#problem_statement').repeater({
        initEmpty: false,
    
        defaultValues: {
            'text-input': 'foo'
        },
    
        show: function () {
            $(this).slideDown();
        },
    
        hide: function (deleteElement) {
            $(this).slideUp(deleteElement);
        }
    });

    $('#url_links').repeater({
        initEmpty: false,
    
        defaultValues: {
            'text-input': 'foo'
        },
    
        show: function () {
            $(this).slideDown();
        },
    
        hide: function (deleteElement) {
            $(this).slideUp(deleteElement);
        }
    });

    $('#project_challenges_points').repeater({
        initEmpty: false,
    
        defaultValues: {
            'text-input': 'foo'
        },
    
        show: function () {
            $(this).slideDown();
        },
    
        hide: function (deleteElement) {
            $(this).slideUp(deleteElement);
        }
    });
    
    $('#outcomes').repeater({
        initEmpty: false,
        defaultValues: false, // Set this to false to use the placeholders instead of default values
    
        show: function () {
            $(this).slideDown();
            // Set the placeholders for the input fields inside the repeater
            $(this).find('input[name="name"]').attr('placeholder', 'Title');
            $(this).find('textarea[name="description"]').attr('placeholder', 'Url');
        },
        hide: function (deleteElement) {
            $(this).slideUp(deleteElement);
        }
    });

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
                    'project_name': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    'service': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    'domain': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    'url': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    
                    'banner_title': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    // 'project_logo': {
                    //     validators: {
                    //         file: {
                    //             maxSize: 1024 * 1024, // Maximum file size in bytes (1 MB)
                    //             message: 'The selected file is not valid or is above 1 MB'
                    //         }
                    //     }
                    // },
                    // 'project_image_banner': {
                    //     validators: {
                    //         file: {
                    //             maxSize: 1024 * 1024, // Maximum file size in bytes (1 MB)
                    //             message: 'The selected file is not valid or is above 1 MB'
                    //         }
                    //     }
                    // },
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
                    'meta_title': {
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
                    // 'og_image': {
                    //     validators: {
                    //         file: {
                    //             maxSize: 1024 * 1024, // Maximum file size in bytes (1 MB)
                    //             message: 'The selected file is not valid or is above 1 MB'
                    //         }
                    //     }
                    // },
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
        
            // Validate form before submit
            
            if (validator) {
                try {
                    const status = await validator.validate();
                    //Project Aim
                    let project_aim = [];
                    // Collect repeater items data
                    const featuresContainer = document.getElementById('features');
                    const repeaterItems = featuresContainer.querySelectorAll('[data-repeater-item]');
                    // Iterate through the repeater items and extract values
                    repeaterItems.forEach((item, index) => {
                        // Select the <input> element inside the current repeater item
                        const inputElement = item.querySelector('[name^="features"][name$="[name]"]');
                    
                        // Extract the input value
                        const inputValue = inputElement ? inputElement.value.trim() : null;
                    
                        // Check if inputValue is not empty before appending
                        if (inputValue !== null && inputValue !== "") {
                            project_aim.push(inputValue);
                        }
                    });
                    //Project Aim End
                    
                    //Problem Statement
                    let problem_statement = [];
                    // Collect repeater items data
                    const ProblemStatementContainer = document.getElementById('problem_statement');
                    const ProblemStatementRepeaterItems = ProblemStatementContainer.querySelectorAll('[data-repeater-item]');
                    // Iterate through the repeater items and extract values
                    ProblemStatementRepeaterItems.forEach((item, index) => {
                        // Select the <input> element inside the current repeater item
                        const inputElement = item.querySelector('[name^="problem_statement"][name$="[name]"]');
                        // Extract the input value
                        const inputValue = inputElement ? inputElement.value.trim() : null;
                    
                        // Check if inputValue is not empty before appending
                        if (inputValue !== null && inputValue !== "") {
                            problem_statement.push(inputValue);
                        }
                    });
                    //Problem Statement End

                    //project_challenges_points
                    let project_challenges_points = [];
                    const EliminatingChallengesContainer = document.getElementById('project_challenges_points');
                    const EliminatingChallengesRepeaterItems = EliminatingChallengesContainer.querySelectorAll('[data-repeater-item]');
                    EliminatingChallengesRepeaterItems.forEach((item, index) => {
                        const inputElement = item.querySelector('[name^="project_challenges_points"][name$="[name]"]');
                        const inputValue = inputElement ? inputElement.value.trim() : null;
                        if (inputValue !== null && inputValue !== "") {
                            project_challenges_points.push(inputValue);
                        }
                    });
                    //end project_challenges_points

                    //outcomes
                    let outcomes = [];
                    const outcomesContainer = document.getElementById('outcomes');
                    const outcomesRepeaterItems = outcomesContainer.querySelectorAll('[data-repeater-item]');
                    outcomesRepeaterItems.forEach((item, index) => {
                    const selectElement = item.querySelector(`[name="outcomes[${index}][name]"]`);
                    const inputElement = item.querySelector(`[name="outcomes[${index}][url]"]`);
                
                    // Extract values
                    const selectValue = selectElement ? selectElement.value : null;
                    const inputValue = inputElement ? inputElement.value : null;
                
                    // Check if both selectValue and inputValue are not empty before appending
                    if (selectValue !== null && inputValue !== null && selectValue !== "" && inputValue !== "") {
                        const itemData = {
                            title: selectValue,
                            url: inputValue,
                        };
                        outcomes.push(itemData);
                    }
                });
                    //outcomes


                    const formData = new FormData();    
                    formData.append('campaigns_id', document.querySelector('[name="campaigns_id"]').value);
                    formData.append('domain', document.querySelector('[name="domain"]').value);
                    formData.append('service', document.querySelector('[name="service"]').value);
                    formData.append('project_name', document.querySelector('[name="project_name"]').value);
                    formData.append('url', document.querySelector('[name="url"]').value);
                    formData.append('project_tags', document.querySelector('[name="project_tags"]').value);
                    formData.append('project_image', document.querySelector('[name="project_image"]').files[0]);

                    //Project Banner
                    formData.append('banner_title', document.querySelector('[name="banner_title"]').value);
                    formData.append('banner_description', CKEDITOR.instances.banner_text.getData());
                    formData.append('project_logo', document.querySelector('[name="project_logo"]').files[0]);
                    formData.append('project_image_banner', document.querySelector('[name="project_image_banner"]').files[0]);

                    //Project Milestone
                    formData.append('research', document.querySelector('[name="research"]').value);
                    formData.append('design_strategy', document.querySelector('[name="design_strategy"]').value);
                    formData.append('ui', document.querySelector('[name="ui"]').value);
                    formData.append('backend_development', document.querySelector('[name="backend_development"]').value);
                    formData.append('frontend_development', document.querySelector('[name="frontend_development"]').value);
                    formData.append('testing', document.querySelector('[name="testing"]').value);

                    //Tech Stack
                    formData.append('front_technology', document.querySelector('[name="front_technology"]').value);
                    formData.append('backend_technology', document.querySelector('[name="backend_technology"]').value);
                    formData.append('other_technology', document.querySelector('[name="other_technology"]').value);

                    //Project Mode Of Functions
                    formData.append('project_mode_of_functions', CKEDITOR.instances.id_content.getData());

                    //Seo
                    formData.append('meta_title', document.querySelector('[name="meta_title"]').value);
                    formData.append('meta_description', document.querySelector('[name="meta_description"]').value);
                    formData.append('meta_keyword', document.querySelector('[name="meta_keyword"]').value);
                    formData.append('meta_image_title', document.querySelector('[name="meta_image_title"]').value);
                    formData.append('og_image', document.querySelector('[name="og_image"]').files[0]);

                    //Eliminating Challenges
                    formData.append('challenges_description', CKEDITOR.instances.eliminating_chanllamges.getData());
                    formData.append('project_challenges_point',JSON.stringify(project_challenges_points))

                    //The OutComes
                    formData.append('web_url_title', document.querySelector('[name="web_url_title"]').value);
                    formData.append('outcome',JSON.stringify(outcomes))

                    //Project Aim
                    formData.append('project_aim', JSON.stringify(project_aim));

                    //Problem Statement
                    formData.append('problem_statement', JSON.stringify(problem_statement));
        
                    submitButton.setAttribute('data-kt-indicator', 'on');
                    submitButton.disabled = true;
        
                    if (status === 'Valid') {
                        const btn = document.getElementById('create-or-update-campaigns-form');
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
        
                        if (data.status === 200) {
                            const redirectUrl = form.getAttribute('data-redirect-url');
                            if (redirectUrl) {
                                location.href = redirectUrl;
                            }
                        } else {
                            // Handle other cases if needed
                            submitButton.removeAttribute('data-kt-indicator');
                            btn.style.display = 'inline-block';
                            loadingBtn.style.display = 'none';
                            submitButton.disabled = false;
        
                            Swal.fire({
                                html: data.message || "please try again.",
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
                            html: data.message || "Sorry, looks like there are some errors detected, please try again.",
                            icon: "error",
                            buttonsStyling: false,
                            confirmButtonText: "Ok, got it!",
                            customClass: {
                                confirmButton: "btn btn-primary"
                            }
                        });
                    }
                } catch (error) {
                    console.error('Error during validation:', error);
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
            // maxFilesize: 1, // MB
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
