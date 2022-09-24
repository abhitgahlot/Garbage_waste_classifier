const options_recycle = {
    style: {
      main: {
        background: "#BEF39A",
        color: "#2C2C2C",
    },
},
};

const options_not_recycle = {
    style: {
      main: {
        background: "#FF7F7F",
        color: "#FFFFEB",
    },
},
};


/*  ==========================================
    SHOW UPLOADED IMAGE
* ========================================== */
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#imageResult').attr('src', e.target.result);
            
            // var optionData = { url: "/image/", method: "post" }
            // optionData["data"] = {'image': e.target.result, }
            // $.ajax({
            //     type: "POST",
            //     url: "/image/",
            //     data: {'image': e.target.result},
            //     success: function (result) {
            //        console.log(result);
            //     }
            //   });
                    
        };
        reader.readAsDataURL(input.files[0]);
        var myFormData = new FormData();
        myFormData.append('pictureFile', input.files[0]);

        $.ajax({
        url: '/image/',
        type: 'POST',
        processData: false, // important
        contentType: false, // important
        dataType : 'json',
        data: myFormData,
        success: function (result) {
            console.log(result);
            if(result.recyclable == "yes"){
                iqwerty.toast.toast(`It is ${result.item} and it is Recyclable`, options_recycle);
            }else{
                iqwerty.toast.toast(`It is ${result.item} and it is not Recyclable`, options_not_recycle);
            }
        }
        });
    }
}

$(function () {
    $('#upload').on('change', function () {
        readURL(input);
    });
});

/*  ==========================================
    SHOW UPLOADED IMAGE NAME
* ========================================== */
var input = document.getElementById( 'upload' );
var infoArea = document.getElementById( 'upload-label' );

input.addEventListener( 'change', showFileName );
function showFileName( event ) {
  var input = event.srcElement;
  var fileName = input.files[0].name;
  infoArea.textContent = 'File name: ' + fileName;
}
