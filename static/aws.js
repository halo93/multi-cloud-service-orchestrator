$(function () {

    $('[data-toggle="tooltip"]').tooltip();

    let chosenBucket;
    let chosenRegion;

    $("#bucket_list_group").on("click", "a.bucket-item", function (event) {
        event.preventDefault();
        if ($(this).attr('class').indexOf('active') <= 0) {
            $("a.bucket-item").removeClass("active");
            $(this).addClass("active");
            chosenBucket = $(this).attr('bucket-name');
            $('#chosen-bucket-name').text(chosenBucket);
            $.get(`api/aws/s3/${chosenBucket}`, function (data) {
                if (data.data) {
                    $('#file_list').empty().append(data.data);
                } else {
                    $('#file_list .panel-body').empty().append('There is no object in this bucket');
                }
            });
        }

    });

    $(document).on("click", "#item_list_group > li > .btn-group > .btn-download", function (event) {
        event.preventDefault();
        const fileName = $(this).attr('file-name');
        $.download(`api/aws/s3/${chosenBucket}/download`, 'file_name', fileName, function () {
            console.log(`Successfully downloaded ${fileName}`);
        });
    });

    $(document).on("click", "#item_list_group > li > .btn-group > .btn-delete", function (event) {
        event.preventDefault();
        const fileName = $(this).attr('file-name');
        $.ajax({
            url: `api/aws/s3/${chosenBucket}`,
            method: 'DELETE',
            contentType: 'application/json',
            data: JSON.stringify({
                file_name: fileName
            }),
            success: function (result) {
                if (result.data) {
                    $('#file_list').empty().append(result.data);
                } else {
                    $('#file_list .panel-body').empty().append('There is no object in this bucket');
                }
            },
            error: function (request, msg, error) {
                console.log(error);
            }
        });
    });

    $(document).on("change", "#validatedCustomFile", function (event) {
        let $labelForFile = $("label[for='validatedCustomFile']");
        if (!event.target.files || event.target.files.length <= 0) {
            $labelForFile.text('Choose file...');
            $(this).closest('.custom-file').find('.invalid-feedback').show();
            return;
        }
        $labelForFile.text(event.target.files[0].name);
        $(this).closest('.custom-file').find('.invalid-feedback').hide();
    });

    $(document).on("click", "#submit-file", function (event) {
        event.preventDefault();
        let $validatedCustomFile = $('#validatedCustomFile');
        let fileProps = $validatedCustomFile.prop('files');
        if (!fileProps || fileProps.length <= 0) {
            $validatedCustomFile.closest('.custom-file').find('.invalid-feedback').show();
        } else {
            $validatedCustomFile.closest('.custom-file').find('.invalid-feedback').hide();
            const formData = new FormData();
            formData.append('file', fileProps[0]);
            $.ajax({
                url: `api/aws/s3/${chosenBucket}`,
                type: "POST",
                data: formData,
                cache: false,
                contentType: false,
                processData: false,
                success: function (response) {
                    console.log(response);
                    $('.modal').modal('hide');
                    $('body').removeClass('modal-open');
                    $('.modal-backdrop').remove();
                    alert("Upload successfully :)");
                    if (response.data) {
                        $('#file_list').empty().append(response.data);
                    } else {
                        $('#file_list .panel-body').empty().append('There is no object in this bucket');
                    }
                },
                error: function(error) {
                    console.log(error);
                    alert("Upload failed :(");
                }
            })
        }
    });

    $(document).on("click", "#v-pills-profile-tab", function (event) {
        $.get(`api/aws/ec2/regions`, function (data) {
            if (data.data) {
                $('#region_list').empty().append(data.data);
            } else {
                $('#region_list .panel-body').empty().append('There is no available region');
            }
        });
        $.get(`api/aws/ec2/regions/all`, function (data) {
            if (data.data) {
                $('#instance_list').empty().append(data.data);
            } else {
                $('#instance_list .panel-body').empty().append('There is no instance created');
            }
        });
    });

    $(document).on("click", "a.region-item", function (event) {
        event.preventDefault();
        if ($(this).attr('class').indexOf('active') <= 0) {
            $("a.region-item").removeClass("active");
            $(this).addClass("active");
            chosenRegion = $(this).attr('region-name');
            $('#chosen-region-name').text(chosenRegion);
            $.get(`api/aws/ec2/regions/${chosenRegion}`, function (data) {
                if (data.data) {
                    $('#instance_list').empty().append(data.data);
                } else {
                    $('#instance_list .panel-body').empty().append('There is no instance created');
                }
            });
        }

    });

    // $(document).on("click", "#instance > li > .btn-group > .btn-delete", function (event) {
    //     event.preventDefault();
    //     if ($(this).attr('class').indexOf('active') <= 0) {
    //         $("a.region-item").removeClass("active");
    //         $(this).addClass("active");
    //         chosenRegion = $(this).attr('region-name');
    //         $('#chosen-region-name').text(chosenRegion);
    //         $.get(`api/aws/ec2/regions/${chosenRegion}`, function (data) {
    //             if (data.data) {
    //                 $('#instance_list').empty().append(data.data);
    //             } else {
    //                 $('#instance_list .panel-body').empty().append('There is no instance created');
    //             }
    //         });
    //     }
    //
    // });
});