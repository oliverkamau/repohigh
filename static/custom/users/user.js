$(document).ready(function () {
    	$.ajaxSetup({
       headers: {
         "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
       }
   });
    searchTeacher();
    searchSupervisor();
    searchUserType();
    supervisorChange();
    userTypeChange();
    saveUser();
    getUsers();
    clearPage();
    editUser();
    deleteUser();
 })
function clearPage() {
    $('#newUser').click(function () {
        clearData()
    })
}
function deleteUser() {
    $('#usersTable').on('click','.btn-deleteUser',function (s) {
        var data = $(this).closest('tr').find('#delete-user').val();
        bootbox.confirm("Are you sure want to delete this User?", function (result) {
            if (result) {
               $.ajax({
            type: 'GET',
            url: 'deleteuser/'+data,
            processData: false,
            contentType: false,
        }).done(function (s) {
          bootbox.hideAll()
          getUsers()
          bootbox.alert(s.success)


        }).fail(function (xhr, error) {
        bootbox.alert(xhr.responseText)
        });
            }
        })
    })
}
function supervisorChange(){
    $('#user_frm').on('select2:select', function (e) {
    var data = e.params.data;
    $('#supervisor').val(data.id)
});
    $("#user_frm").on("select2:unselecting", function(e) {
    $('#supervisor').val('')
 });
}
function userTypeChange(){
    $('#usertype_frm').on('select2:select', function (e) {
    var data = e.params.data;
    $('#userType').val(data.id)

});
    $('#usertype_frm').on("select2:unselecting", function(e) {
    $('#userType').val('')
 });
}
function searchTeacher() {
     $('#teacher_frm').select2({
           placeholder: 'Select From Teachers',
           allowClear: true,
           ajax: {
             delay: 250,
             url: 'searchteachers',
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
function searchUserType() {
     $('#usertype_frm').select2({
           placeholder: 'UserType',
           allowClear: true,
           ajax: {
             delay: 250,
             url: 'searchtypes',
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
function searchSupervisor() {
     $('#user_frm').select2({
           placeholder: 'Supervisor',
           allowClear: true,
           ajax: {
             delay: 250,
             url: 'searchsupervisor',
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

function saveUser(){
    $('#saveUser').click(function () {
        var data=$('#user-form').serialize();
        var url = '';
        if($('#userCode').val()===''){
          url = 'createuser'
        }else{
            url = 'updateuser/'+$('#userCode').val()
        }
		$.ajax({
			type: 'POST',
			url: url,
            data: data
		}).done(function (s) {
		    getUsers()
            clearData()
			bootbox.alert(s.success)

		}).fail(function (xhr, error) {
		       console.log(error)
                bootbox.alert(xhr.responseText)
		})


	})
}
function editUser(){
    $('#usersTable').on('click','.btn-editUser',function (s) {
        var data=$(this).closest('tr').find('#edit-user').val();
        $.ajax({
            type: 'GET',
            url: 'editusers/'+data,
            processData: false,
            contentType: false,
        }).done(function (s) {
            $('#userCode').val(s.userId);
            $('#firstName').val(s.userFname);
            $('#lastName').val(s.userLname);
            $('#gender').val(s.userGender);
            $('#email').val(s.email);
            $('#phone').val(s.userPhone);
            $('#address').val(s.userAddress);
            $('#userName').val(s.userName);
            $('#userName').prop('disabled',true);
            $('#password').prop('disabled',true);
            if (s.status === true) {
                $('#active').prop('checked', true);
            }
            else {
                $('#active').prop('checked', false);

            }
            if (s.userTypeCode) {
                $('#userType').val(s.userTypeCode)
                var $newClass = $("<option selected='selected' value='" + s.userTypeCode + "'>'+s.userTypeName+'</option>").val(s.userTypeCode.toString()).text(s.userTypeName)

                $('#usertype_frm').append($newClass).trigger('change');
            }
            else {
                $('#userType').val('')
                $('#usertype_frm').empty();
            }
            if (s.supervisorCode) {
                $('#supervisor').val(s.supervisorCode)
                var $newVisor = $("<option selected='selected' value='" + s.supervisorCode + "'>'+s.supervisorName+'</option>").val(s.supervisorCode.toString()).text(s.supervisorName)

                $('#user_frm').append($newVisor).trigger('change');
            }
            else {
                $('#supervisor').val('')
                $('#user_frm').empty();
            }
            if (s.teacherCode) {
                $('#teacher-id').val(s.teacherCode)
                var $newTeacher = $("<option selected='selected' value='" + s.teacherCode + "'>'+s.teacherName+'</option>").val(s.teacherCode.toString()).text(s.teacherName)

                $('#teacher_frm').append($newClass).trigger('change');
            }
            else {
                $('#teacher-id').val('')
                $('#teacher_frm').empty();
            }
            }).fail(function (xhr, error) {

        bootbox.alert(xhr.responseText)
        });
    });

}

function clearData(){
      $('#usertype_frm').empty();
      $('#user_frm').empty();
      $('#teacher_frm').empty();
      $('#userType').val('');
      $('#teacher-id').val('');
      $('#supervisor').val('');
      $('#user-form')[0].reset();
      $('#userName').prop('disabled',false);
      $('#password').prop('disabled',false);
}
function getUsers() {
     $.ajax({
        type: 'GET',
        url: 'getusers',
        processData: false,
        contentType: false,
    }).done(function (s) {
       $('#usersTable').DataTable().destroy();
       $("#usersTable tbody").empty();
        if(s.length!==0) {
            $.each(s, function (i, item) {
                $("#usersTable tbody").append(
                    "<tr>"
                    + "<td>" + item.userName + "</td>"
                    + "<td>" + item.userType + "</td>"
                    + "<td>" + item.userFname + "</td>"
                    + "<td>" + item.userLname + "</td>"
                    + "<td>" + item.userGender + "</td>"
                    + "<td>" + item.email + "</td>"
                    + "<td>" + item.userAddress + "</td>"
                    + "<td>" + item.userPhone + "</td>"
                    + "<td>" + item.supervisorName + "</td>"
                    + "<td>" + item.status + "</td>"
                    + "<td>" + '<form id="editForm" method="post" enctype="multipart/form-data"><input type="hidden" id="edit-user" name="id" value=' + item.userId + '></form><button class="btn btn-outline-primary btn-sm btn-editUser" ><i class="fa fa-edit"></button>'
                    + "</td>"
                    + "<td>" + '<form id="deleteForm" method="post" enctype="multipart/form-data"><input type="hidden" id="delete-user" name="id" value=' + item.userId + '></form><button class="btn btn-outline-danger btn-sm btn-deleteUser" ><i class="fa fa-trash-o"></button>'
                    + "</tr>")
            })
        }
        $('#usersTable').DataTable();
    }).fail(function (xhr, error) {
       bootbox.alert(xhr.responseText);
    });

}