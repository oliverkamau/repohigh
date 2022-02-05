$(document).ready(function () {
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        }
    });
orgLogo("")
saveOrganization()
    newOrganization()
    getOrganization()
    deleteOrganization()
    editOrganization()
})
function orgLogo(url){
        $("#org-avatar").fileinput('destroy').fileinput({
            overwriteInitial: true,
            maxFileSize: 1500,
            showClose: false,
            showCaption: false,
            showBrowse: true,
            browseLabel: '',
            removeLabel: '',
            browseIcon: '<i class="fa fa-folder-open"></i>',
            removeIcon: '',
            removeTitle: 'Cancel or reset changes',
            elErrorContainer: '#kv-avatar-errors',
            msgErrorClass: 'alert alert-block alert-danger',
            defaultPreviewContent: '<img src="' + url + '"  style="height:15em;width:225px">',
            layoutTemplates: {main2: '{preview} ' + ' {remove} {browse}'},
            allowedFileExtensions: ["jpg", "png", "gif"]
        });

}
function newOrganization(){
    $('#newOrganization').click(function () {
        clearpage();
    })
}
function saveOrganization(){
    $('#saveOrganization').click(function () {

        if($('#organizationName').val()==''){
         swal({
          title: 'Alert!',
          type: 'info',
          text: 'Organization Name Field is Mandatory',
         confirmButtonText: 'OK'
      })
        }
        else if($('#telNo').val()==='') {
            swal({
                title: 'Alert!',
                type: 'info',
                text: 'Telephone Number Field is Mandatory',
                confirmButtonText: 'OK'
            })
        }
         else if($('#cellNo').val()===''){
           swal({
          title: 'Alert!',
          type: 'info',
          text: 'Cellphone Field is Mandatory',
         confirmButtonText: 'OK'
      })
        }
         else if($('#email').val()===''){
           swal({
          title: 'Alert!',
          type: 'info',
          text: 'Email Field is Mandatory',
         confirmButtonText: 'OK'
      })
        }
        else {
            var form = $("#organization-form")[0];
            var data = new FormData(form);
            data.append('organization_logo', $('#org-avatar')[0].files[0]);
            var url = '';
            if ($('#organizationCode').val() === '') {
                url = 'addorganization'
            } else {
                url = 'updateorganization/' + $('#organizationCode').val()
            }
            $.ajax({
                type: 'POST',
                url: url,
                data: data,
                processData: false,
                contentType: false
            }).done(function (s) {
                clearpage();
                swal({
                    type: 'success',
                    title: 'Success',
                    text: s.success,
                    showConfirmButton: true
                })
              getOrganization()

            }).fail(function (xhr, error) {
                bootbox.alert(xhr.responseText)
                // bootbox.alert("Error Occured while saving")
            })

        }
	})
}
function clearpage(){
    $('#organization-form')[0].reset();
    $('#organizationCode').val('');
    orgLogo("")
}
function getOrganization() {
     $.ajax({
        type: 'GET',
        url: 'getorganizations',
        processData: false,
        contentType: false,
    }).done(function (s) {
       $('#orgTable').DataTable().destroy();
       $("#orgTable tbody").empty();
        if(s.length!==0) {
            $.each(s, function (i, item) {
                $("#orgTable tbody").append(
                    "<tr scope='col'>"
                   + "<td>" + '<form id="editForm" method="post" enctype="multipart/form-data"><input type="hidden" id="edit-org" name="id" value=' + item.code + '></form><button class="btn btn-outline-primary btn-sm btn-editOrg" ><i class="fa fa-edit"></button>'
                    + "</td>"
                    + "<td>" + '<form id="deleteForm" method="post" enctype="multipart/form-data"><input type="hidden" id="delete-org" name="id" value=' + item.code + '></form><button class="btn btn-outline-danger btn-sm btn-deleteOrg" ><i class="fa fa-trash-o"></button>'
                     + "</td>"
                    + "<td>" + item.name + "</td>"
                    + "<td>" + item.telno + "</td>"
                    + "<td>" + item.cellno + "</td>"
                    + "<td>" + item.email + "</td>"
                   + "<td>" + item.websites + "</td>"
                    + "</tr>")
            })
        }
        $('#orgTable').DataTable();
    }).fail(function (xhr, error) {
       bootbox.alert(xhr.responseText);
    });

}
function deleteOrganization() {
     $('#orgTable').on('click','.btn-deleteOrg',function (s) {
        var data = $(this).closest('tr').find('#delete-org').val();
        bootbox.confirm("Are you sure want to delete this Organization?", function (result) {
            if (result) {
               $.ajax({
            type: 'GET',
            url: 'deleteorganization/'+data,
            processData: false,
            contentType: false,
        }).done(function (s) {
          getOrganization()
          swal({
                    type: 'success',
                    title: 'Success',
                    text: s.success,
                    showConfirmButton: true
                })

        }).fail(function (xhr, error) {
        bootbox.alert(xhr.responseText)
        });
            }
        })
    })
}
function editOrganization(){
    $('#orgTable').on('click','.btn-editOrg',function (s) {
        var data=$(this).closest('tr').find('#edit-org').val();
        $.ajax({
            type: 'GET',
            url: 'editorganization/'+data,
            processData: false,
            contentType: false,
        }).done(function (s) {
            $('#organizationCode').val(s.code);
            $('#organizationName').val(s.name);
            $('#physicalAddress').val(s.address);
            $('#postalAddress').val(s.postal);
            $('#telNo').val(s.telno);
            $('#cellNo').val(s.cellno);
            $('#websites').val(s.websites);
            $('#email').val(s.email);
            $('#mission').val(s.mission);
            $('#vision').val(s.vision);
            $('#motto').val(s.motto);
			if(s.url) {
                orgLogo(s.url)
            }
            else{
			    orgLogo("")
            }
        }).fail(function (xhr, error) {
        bootbox.alert(xhr.responseText)
        });
    });

}