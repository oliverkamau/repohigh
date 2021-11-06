$(document).ready(function () {
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        }
    });
    parentImage("");
    searchProffession();
    searchMotherProffession();
    getParents();
    saveParent();
    parentChange();
    editParent();
    deleteParent();
    newParent();
    importparents();
    downloadparents();
})
function newParent() {
   $('#newParent').click(function () {
       clearData()
       parentImage("");
   })
}
function deleteParent() {
    $('#parTable').on('click','.btn-deleteParent',function (s) {
        var data = $(this).closest('tr').find('#delete-parent').val();
        if(data===''){
           bootbox.alert('No Parent Selected For Deletion')
        }
        else {
            bootbox.confirm("Are you sure want to delete this Parent?", function (result) {
                if (result) {
                    $.ajax({
                        type: 'GET',
                        url: 'deleteparents/' + data,
                        processData: false,
                        contentType: false,
                    }).done(function (s) {
                        bootbox.hideAll()
                        getParents()
                        bootbox.alert(s.success)


                    }).fail(function (xhr, error) {
                        bootbox.alert(xhr.responseText)
                    });
                }
            })
        }
    })

}
function importparents(){
    $("#btn-import-parent").change(function(e){
			var selectedFile= e.target.files[0];
			 var data = new FormData();
            data.append('file', selectedFile);
            var url = 'importexcel';
            $.ajax({
                type: 'POST',
                url: url,
                data: data,
                processData: false,
                contentType: false
                // data: {
                // 	'firstName':$('#inputFirstname').val(),
                // 	'lastName':$('#inputLastname').val(),
                // 	'age':$('#inputAge').val(),
                // 	'height':$('#inputHeight').val(),
                // 	'country':$('#inputCountry').val(),
                // 	'county':$('#inputCounty').val(),
                // 	'town':$('#inputTown').val(),
                // 	'phone':$('#inputPhone').val(),
                // 	'website':$('#inputWebsite').val(),
                // }
            }).done(function (s) {
                getParents();
                clearData();
                bootbox.alert(s.success)

            }).fail(function (xhr, error) {
                p=JSON.parse(xhr.responseText)

                console.log(p.error)
                bootbox.alert(p.error)
                // bootbox.alert("Error Occured while saving")
            })

        })
}
function downloadparents(){
    $("#downloadParent").click(function(e){
            var url = 'downloadexcel';
            $.ajax({
                type: 'GET',
                url: url
                // data: {
                // 	'firstName':$('#inputFirstname').val(),
                // 	'lastName':$('#inputLastname').val(),
                // 	'age':$('#inputAge').val(),
                // 	'height':$('#inputHeight').val(),
                // 	'country':$('#inputCountry').val(),
                // 	'county':$('#inputCounty').val(),
                // 	'town':$('#inputTown').val(),
                // 	'phone':$('#inputPhone').val(),
                // 	'website':$('#inputWebsite').val(),
                // }
            }).done(function (s) {
                // getParents();
                // clearData();
                // bootbox.alert(s.success)

            }).fail(function (xhr, error) {
                // p=JSON.parse(xhr.responseText)
                //
                // console.log(p.error)
                // bootbox.alert(p.error)
                bootbox.alert("Error Occured excelling")
            })

        })
}
function editParent(){
    $('#parTable').on('click','.btn-editParent',function (s) {
        var data=$(this).closest('tr').find('#edit-parent').val();
        $.ajax({
            type: 'GET',
            url: 'editparents/'+data,
            processData: false,
            contentType: false,
        }).done(function (s) {
           $('#parentCode').val(s.parentCode);
            $('#fatherName').val(s.fatherName);
			$('#fatherAddress').val(s.fatherAddress);
			$('#fatherPhone').val(s.fatherPhone);
			$('#fatherEmail').val(s.fatherEmail);
			$('#motherName').val(s.motherName);
			$('#motherAddress').val(s.motherAddress);
			$('#motherPhone').val(s.motherPhone);
			$('#motherEmail').val(s.motherEmail);
			$('#parentType').val(s.parentType);
			$('#idNo').val(s.idNo);
			if (s.emailRequired === true) {
                $('#emailRequired').prop('checked', true);
            }
            else {
                $('#emailRequired').prop('checked', false);

            }
			if (s.fatherProfId) {
			    var $newCountry = $("<option selected='selected' value='" + s.fatherProfId + "'>'+s.fatherProfName+'</option>").val(s.fatherProfId.toString()).text(s.fatherProfName)

               $('#prf-frm').append($newCountry).trigger('change');
			    $('#fatherProffession').val(s.fatherProfId)
			    }
			    else {
			    $('#prf-frm').empty();
			    $('#fatherProffession').val('')

			}
			if (s.motherProfId) {
			    var $newOption = $("<option selected='selected' value='" + s.motherProfId + "'>'+s.motherProfName+'</option>").val(s.motherProfId.toString()).text(s.motherProfName)

               $('#prm-frm').append($newOption).trigger('change');
			   $('#motherProffession').val(s.motherProfId)

			    } else {
			    $('#prm-frm').empty();
			    $('#motherProffession').val('')

			}
			if(s.url) {
                parentImage(s.url)
            }
            else{
			    parentImage("")
            }

        }).fail(function (xhr, error) {
        bootbox.alert(xhr.responseText)
        });
    });

}
function parentChange(){
     $('#prm-frm').on('select2:select', function (e) {
    var data = e.params.data;
    $('#motherProffession').val(data.id)
});
    $("#prm-frm").on("select2:unselecting", function(e) {
    $('#motherProffession').val('')
 });
     $('#prf-frm').on('select2:select', function (e) {
    var data = e.params.data;
    $('#fatherProffession').val(data.id)
});
    $("#prf-frm").on("select2:unselecting", function(e) {
    $('#fatherProffession').val('')
 });
}
function clearData(){
      $('#prm-frm').empty();
      $('#motherProffession').val('');
      $('#parentCode').val('');
      $('#parent-form')[0].reset();
      $('#prf-frm').empty();
      $('#fatherProffession').val('');
}
function saveParent(){
    $('#saveParent').click(function () {
        if($('#fatherName').val()==='' || $('#fatherPhone').val()==='' || $('#idNo').val()===''){
            bootbox.alert('Please Provide data to save !!!')
        }
        else {
            var form = $("#parent-form")[0];
            var data = new FormData(form);
            data.append('parent_photo', $('#parent-avatar')[0].files[0]);
            var url = '';
            if ($('#parentCode').val() === '') {
                url = 'addparents'
            } else {
                url = 'updateparents/' + $('#parentCode').val()
            }
            $.ajax({
                type: 'POST',
                url: url,
                data: data,
                processData: false,
                contentType: false
                // data: {
                // 	'firstName':$('#inputFirstname').val(),
                // 	'lastName':$('#inputLastname').val(),
                // 	'age':$('#inputAge').val(),
                // 	'height':$('#inputHeight').val(),
                // 	'country':$('#inputCountry').val(),
                // 	'county':$('#inputCounty').val(),
                // 	'town':$('#inputTown').val(),
                // 	'phone':$('#inputPhone').val(),
                // 	'website':$('#inputWebsite').val(),
                // }
            }).done(function (s) {
                getParents();
                clearData();
                bootbox.alert(s.success)

            }).fail(function (xhr, error) {
                bootbox.alert(xhr.responseText)
                // bootbox.alert("Error Occured while saving")
            })

        }
	})
}
function getParents() {
     $.ajax({
        type: 'GET',
        url: 'getparents',
        processData: false,
        contentType: false,
    }).done(function (s) {
       $('#parTable').DataTable().destroy();
       $("#parTable tbody").empty();
        if(s.length!==0) {
            $.each(s, function (i, item) {
                $("#parTable tbody").append(
                    "<tr scope='col'>"
                    + "<td>" + item.fatherName + "</td>"
                    + "<td>" + item.fatherAddress + "</td>"
                    + "<td>" + item.fatherPhone + "</td>"
                    + "<td>" + item.fatherProfName + "</td>"
                    + "<td>" + item.fatherEmail + "</td>"
                    + "<td>" + item.parentType + "</td>"
                    + "<td>" + item.motherName + "</td>"
                    + "<td>" + item.motherAddress + "</td>"
                    + "<td>" + item.motherPhone + "</td>"
                    + "<td>" + item.motherProfName + "</td>"
                    + "<td>" + item.motherEmail + "</td>"
                    + "<td>" + item.emailRequired + "</td>"
                    + "<td>" + item.idNo + "</td>"
                    + "<td>" + '<form id="editForm" method="post" enctype="multipart/form-data"><input type="hidden" id="edit-parent" name="id" value=' + item.parentCode + '></form><button class="btn btn-outline-primary btn-sm btn-editParent" ><i class="fa fa-edit"></button>'
                    + "</td>"
                    + "<td>" + '<form id="deleteForm" method="post" enctype="multipart/form-data"><input type="hidden" id="delete-parent" name="id" value=' + item.parentCode + '></form><button class="btn btn-outline-danger btn-sm btn-deleteParent" ><i class="fa fa-trash-o"></button>'
                    + "</tr>")
            })
        }
        $('#parTable').DataTable();
    }).fail(function (xhr, error) {
       bootbox.alert(xhr.responseText);
    });

}

function searchProffession() {
     $('#prf-frm').select2({
           placeholder: 'Proffession',
           allowClear: true,
           ajax: {
             delay: 250,
             url: 'searchproffession',
             data: function (params) {
                 console.log("AA", params);
                 return {
                     query: params.term,
                     gotoPage: params.page
                 }
             },

             processResults: function (data,params) {
                 params.page = params.page || 1;
                 console.log('data: ', data);
                 return {
                   results: data.results
                 };
             }

         }
     })
}
function searchMotherProffession() {
     $('#prm-frm').select2({
           placeholder: 'Proffession',
           allowClear: true,
           ajax: {
             delay: 250,
             url: 'searchproffession',
             data: function (params) {
                 console.log("AA", params);
                 return {
                     query: params.term,
                     gotoPage: params.page
                 }
             },

             processResults: function (data,params) {
                 params.page = params.page || 1;
                 console.log('data: ', data);
                 return {
                   results: data.results
                 };
             }

         }
     })
}
function parentImage(url){
    console.log(url)
        $("#parent-avatar").fileinput('destroy').fileinput({
            overwriteInitial: true,
            maxFileSize: 1500,
            showClose: false,
            showCaption: false,
            browseLabel: '',
            removeLabel: '',
            browseIcon: '<i class="fa fa-folder-open"></i>',
            removeIcon: '<i class="fa fa-times"></i>',
            removeTitle: 'Cancel or reset changes',
            elErrorContainer: '#kv-avatar-errors',
            msgErrorClass: 'alert alert-block alert-danger',
            defaultPreviewContent: '<img src="' + url + '"  style="height:15em;width:200px">',
            layoutTemplates: {main2: '{preview} ' + ' {remove} {browse}'},
            allowedFileExtensions: ["jpg", "png", "gif"]
        });

}