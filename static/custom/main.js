

$(document).ready(function () {
    	$.ajaxSetup({
       headers: {
         "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
       }
   });
    getStudents();
    editStudent();
    saveStudent();
    deleteStudent();
    searchStudent();
    studentChange();
    saveCountry();
    saveCounty();
    getCountries();
    searchCountries();
    countryChange();
    getCounties();
    countyChange()
    parentImage("");

   $('#sidebarCollapse').on('click',function () {
       $('#sidebar').toggleClass('active');
   })


 })
function studentChange(){
    $('#search-frm').on('select2:select', function (e) {
    var data = e.params.data;
    $('#stud-id').val(e.params.data.id)
    $('#stud-name').val(e.params.data.text)

});
    $("#search-frm").on("select2:unselecting", function(e) {
    $('#stud-id').val('')
    $('#stud-name').val('')
 });
}
function countyChange(){
    $('#county-frm').on('select2:select', function (e) {
    var data = e.params.data;
    $('#county-id').val(e.params.data.id)
    $('#county-name').val(e.params.data.text)

});
    $("#search-frm").on("select2:unselecting", function(e) {
    $('#county-id').val('')
    $('#county-name').val('')
 });
}
function countryChange(){
    $('#country-frm').on('select2:select', function (e) {
    var data = e.params.data;
    $('#country-id').val(e.params.data.id)
    $('#country-name').val(e.params.data.text)

    // console.log('country is: '+$('#country-id').val())
        searchCounty(data.id)

});
    $("#country-frm").on("select2:unselecting", function(e) {
    $('#country-id').val('')
    $('#country-name').val('')
 });
}
function searchStudent() {
     $('#search-frm').select2({
           placeholder: 'Students',
           allowClear: true,
           ajax: {
             delay: 250,
             url: 'searchStudents',
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

// function getCountry() {
//     console.log($('#country-id').val())
//     return 'searchCounties/'+$('#country-id').val()
// }

function searchCounty(id) {
        $('#county-frm').select2({
            placeholder: 'Counties',
            allowClear: true,
            ajax: {
                delay: 250,
                url: 'searchCounties/'+id,
                data: function (params) {
                    console.log("AA", params);
                    return {
                        query: params.term,
                        gotoPage: params.page
                    }
                },

                processResults: function (data, params) {
                    params.page = params.page || 1;
                    console.log('data: ', data);
                    return {
                        results: data.results
                    };
                }

            }
        })

}
function searchCountries() {
     $('#country-frm').select2({
           placeholder: 'Countries',
           allowClear: true,
           ajax: {
             delay: 250,
             url: 'searchCountries',
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
            defaultPreviewContent: '<img src="' + url + '"  style="height:13em;width:230px">',
            layoutTemplates: {main2: '{preview} ' + ' {remove} {browse}'},
            allowedFileExtensions: ["jpg", "png", "gif"]
        });

}
function deleteStudent() {
    $('#studTable').on('click','.btn-deletestudent',function (s) {
        var data = $(this).closest('tr').find('#delete-student').val();
        bootbox.confirm("Are you sure want to delete this student?", function (result) {
            if (result) {
               $.ajax({
            type: 'GET',
            url: 'deleteStudent/'+data,
            processData: false,
            contentType: false,
        }).done(function (s) {
            getStudents()
          bootbox.alert(s.success)

        }).fail(function (xhr, error) {
        bootbox.alert(xhr.responseText)
        });
            }
        })
    })
}

function getStudents() {
     $.ajax({
        type: 'GET',
        url: 'getStudents',
        processData: false,
        contentType: false,
    }).done(function (s) {
        $("#studTable tbody").empty();
        $.each(s,function(i,item){
            $("#studTable tbody").append(
                "<tr>"
                +"<td>"+item.name+"</td>"
                +"<td>"+item.age+"</td>"
                +"<td>"+item.country_name+"</td>"
                +"<td>"+item.county_name+"</td>"
                +"<td>"+item.town+"</td>"
                +"<td>"+item.phone+"</td>"
                +"<td>"+item.website+"</td>"
                +"<td>"+'<form id="editForm" method="post" enctype="multipart/form-data"><input type="hidden" id="edit-student" name="id" value='+item.stdCode+'></form><button class="btn btn-outline-primary btn-sm btn-editstudent" ><i class="fa fa-edit"></button>'
                +"</td>"
                +"<td>"+'<form id="deleteForm" method="post" enctype="multipart/form-data"><input type="hidden" id="delete-student" name="id" value='+item.stdCode+'></form><button class="btn btn-outline-danger btn-sm btn-deletestudent" ><i class="fa fa-trash-o"></button>'
                +"</tr>" )
        })
        $('#studTable').DataTable();
    }).fail(function (xhr, error) {
       bootbox.alert(xhr.responseText);
    });

}

function saveStudent(){
    $('#save-stud').click(function () {
       var form = $("#student-form")[0];
		var data = new FormData( form );
		data.append( 'photo', $( '#parent-avatar' )[0].files[0] );
		var url = '';
        if($('#inputCode').val()===''){
          url = 'add'
        }else{
            url = 'update/'+$('#inputCode').val()
        }
		$.ajax({
			type: 'POST',
			url: url,
            data: data,
            processData: false,
            contentType: false
		}).done(function (s) {
		    getStudents()
			bootbox.alert(s.success)

		}).fail(function (xhr, error) {
						bootbox.alert(xhr.responseText)
            // bootbox.alert("Error Occured while saving")
		})


	})
}

function getCountries() {
     $.ajax({
        type: 'GET',
        url: 'getCountries',
        processData: false,
        contentType: false,
    }).done(function (s) {
        $("#countryTable tbody").empty();
        $.each(s,function(i,item){
            $("#countryTable tbody").append(
                "<tr>"
                +"<td>"+item.fields.country_name+"</td>"
                +"<td>"+item.fields.country_code+"</td>"
                +"<td>"+item.fields.country_continent+"</td>"
                +"<td>"+'<form id="editForm" method="post" enctype="multipart/form-data"><input type="hidden" id="edit-student" name="id" value='+item.pk+'></form><button class="btn btn-outline-primary btn-sm btn-editstudent" ><i class="fa fa-edit"></button>'
                +"</td>"
                +"<td>"+'<form id="deleteForm" method="post" enctype="multipart/form-data"><input type="hidden" id="delete-student" name="id" value='+item.pk+'></form><button class="btn btn-outline-danger btn-sm btn-deletestudent" ><i class="fa fa-trash-o"></button>'
                +"</tr>" )
        })
        $('#countryTable').DataTable();
    }).fail(function (xhr, error) {
       bootbox.alert(xhr.responseText);
    });

}
function getCounties() {
     $.ajax({
        type: 'GET',
        url: 'getCounties',
        processData: false,
        contentType: false,
    }).done(function (s) {
        $("#countyTable tbody").empty();
        $.each(s,function(i,item){
            console.log(s)
            console.log(i)
            console.log(s[i].county_name)
            $("#countyTable tbody").append(
                "<tr>"
                +"<td>"+item.county_name+"</td>"
                +"<td>"+item.county_code+"</td>"
                +"<td>"+item.country_name+"</td>"
                +"<td>"+'<form id="editForm" method="post" enctype="multipart/form-data"><input type="hidden" id="edit-student" name="id" value='+item.pk+'></form><button class="btn btn-outline-primary btn-sm btn-editstudent" ><i class="fa fa-edit"></button>'
                +"</td>"
                +"<td>"+'<form id="deleteForm" method="post" enctype="multipart/form-data"><input type="hidden" id="delete-student" name="id" value='+item.pk+'></form><button class="btn btn-outline-danger btn-sm btn-deletestudent" ><i class="fa fa-trash-o"></button>'
                +"</tr>" )
        })
        $('#countryTable').DataTable();
    }).fail(function (xhr, error) {
       bootbox.alert(xhr.responseText);
    });

}
function saveCountry(){
    $('#save-country').click(function () {
        var data=$('#country-form').serialize();
        var url = '';
        if($('#inputId').val()===''){
          url = 'addCountry'
        }else{
            url = 'updateCountry/'+$('#inputId').val()
        }
		$.ajax({
			type: 'POST',
			url: url,
            data: data
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
		    getCountries()
			bootbox.alert(s.success)

		}).fail(function (xhr, error) {
						bootbox.alert(xhr.responseText)
            // bootbox.alert("Error Occured while saving")
		})


	})
}
function saveCounty(){
    $('#save-county').click(function () {
        var data=$('#county-form').serialize();
        var url = '';
        if($('#inputId').val()===''){
          url = 'addCounty'
        }else{
            url = 'updateCounty/'+$('#inputId').val()
        }
		$.ajax({
			type: 'POST',
			url: url,
            data: data
		}).done(function (s) {
		    getCounties()
			bootbox.alert(s.success)

		}).fail(function (xhr, error) {
						bootbox.alert(xhr.responseText)
            // bootbox.alert("Error Occured while saving")
		})


	})
}
function editStudent(){
    $('#studTable').on('click','.btn-editstudent',function (s) {
        var data=$(this).closest('tr').find('#edit-student').val();
        $.ajax({
            type: 'GET',
            url: 'editStudent/'+data,
            processData: false,
            contentType: false,
        }).done(function (s) {
           $('#inputCode').val(s.stdCode);
            $('#inputFirstname').val(s.firstName);
			$('#inputLastname').val(s.lastName);
			$('#inputAge').val(s.age);
			$('#inputHeight').val(s.height);
			$('#country-id').val(s.country_id);
			$('#county-id').val(s.county_id);
			$('#inputTown').val(s.town);
			$('#inputPhone').val(s.phone);
			$('#inputWebsite').val(s.website);
			$('#county-frm').select2();
			if (s.country_id) {
			    var $newCountry = $("<option selected='selected' value='" + s.country_id + "'>'+s.country_name+'</option>").val(s.country_id.toString()).text(s.country_name)

               $('#country-frm').append($newCountry).trigger('change');
			    }
			    else {
			    $('#country-frm').empty();
			}
			if (s.county_id) {
			    var $newOption = $("<option selected='selected' value='" + s.county_id + "'>'+s.county_name+'</option>").val(s.county_id.toString()).text(s.county_name)

               $('#county-frm').append($newOption).trigger('change');
			    } else {
			    $('#county-frm').empty();
			}
            parentImage(s.url)

        }).fail(function (xhr, error) {
        bootbox.alert(xhr.responseText)
        });
    });

}