$(document).ready(function () {
        $.ajaxSetup({
            headers: {
                "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
            }
        });
searchTerm();
termChange();
yearChange();
examChange();
classChange();
formatDate();
teacherChange();
subjectChange();
studentChange();
calculateMarks();
 getIntialExamMarks();
saveMarks();
editMarks();
deleteMarks();
clearData();
getDynamicUrl();
importmarks();
$('#exportBtn').prop('disabled',true)
})
function getIntialExamMarks() {
    $('#processTable').DataTable({})
}
function clearData(){
    $('#newMarks').click(function () {
        $('#marks').val('')
        $('#examRemarks').val('')
        $('#examPercentageMarks').val('')
        $('#displayName').val('')
    $('#processing-form')[0].reset();
    $('#reg_frm').empty();
    $('#year_frm').empty();
    $('#grading_frm').empty();
    $('#term_frm').empty();
    $('#class_frm').empty();
    $('#teacher_frm').empty();
    $('#student_frm').empty();
    $('#subject_frm').empty();
    $('#regCode').val('');
    $('#gradeCode').val('');
    $('#processCode').val('');
    $('#yearCode').val('');
    $('#teacherCode').val('');
    $('#classCode').val('');
    $('#termCode').val('');
    $('#studentCode').val('');
    $('#subjectCode').val('');
    $('#examExcelClass').val('');
    $('#examExcelSubject').val('');
    $('#examExcelCode').val('');
    $('#examExcelTeacher').val('');
    $('#exportBtn').prop('disabled',true)

    formatDate()
    })
}
function formatDate() {
    var d = new Date(),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2)
        month = '0' + month;
    if (day.length < 2)
        day = '0' + day;

    $('#examDate').val([year, month, day].join('-'));

}
function teacherChange() {
    $('#teacher_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#teacherCode').val(data.id)
        $('#examExcelTeacher').val(data.id)
        searchSubjects($('#classCode').val(),data.id);
    });
    $("#teacher_frm").on("select2:unselecting", function(e) {
    $('#teacherCode').val('')
 });
}
function searchTeacher() {
        $('#teacher_frm').select2({
            placeholder: 'Teachers',
            allowClear: true,
            width: '67%',
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
function searchSubjects(id,teacher) {

        $('#subject_frm').select2({
            placeholder: 'Subjects',
            allowClear: true,
            width: '67%',
            ajax: {
                delay: 250,
                url: 'searchsubjects/'+id+'/'+teacher,
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
function subjectChange() {

    $('#subject_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#subjectCode').val(data.id)
        $('#examExcelSubject').val(data.id)
        searchStudent($('#classCode').val(),data.id)
        $('#exportBtn').prop('disabled',false)

    });
    $("#subject_frm").on("select2:unselecting", function(e) {
    $('#subjectCode').val('')
 });

}
function searchStudent(id,subject) {

        $('#student_frm').select2({
            placeholder: 'Students',
            allowClear: true,
            width: '67%',
            ajax: {
                delay: 250,
                url: 'searchstudents/'+id+'/'+subject,
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

function studentChange() {
    $('#student_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#studentCode').val(data.id)
    });
    $("#student_frm").on("select2:unselecting", function(e) {
    $('#studentCode').val('')
 });
}

function searchTerm() {

        $('#term_frm').select2({
            placeholder: 'Term',
            allowClear: true,
                        width: '67%',

            ajax: {
                delay: 250,
                url: 'searchexamterm',
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

function yearChange() {
    $('#year_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#yearCode').val(data.id)
         searchExam($('#termCode').val(),data.id)

    });
    $("#year_frm").on("select2:unselecting", function(e) {
    $('#yearCode').val('')
    $('#yearName').val('')

 });
}
function searchYear() {
        $('#year_frm').select2({
            placeholder: 'Year',
            allowClear: true,
            width: '66%',
            ajax: {
                delay: 250,
                url: 'searchexamyear',
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
function searchGrading() {
        $('#grading_frm').select2({
            placeholder: 'Grading',
            allowClear: true,
                        width: '67%',

            ajax: {
                delay: 250,
                url: 'searchexamgrading',
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
function gradingChange() {
    $('#class_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#classCode').val(data.id)
     searchTeacher();
    });
    $("#class_frm").on("select2:unselecting", function(e) {
    $('#classCode').val('')
 });
}
function searchClass() {
        $('#class_frm').select2({
            placeholder: 'Select Class',
            allowClear: true,
            ajax: {
                delay: 250,
                url: 'searchclasses',
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
function getDynamicUrl() {
   $.ajax({
          type: 'GET',
          url: 'dynamicaddress',
      }).done(function (s) {
          spinner=s.url
      }).fail(function (xhr, error) {
          bootbox.alert(xhr.responseText)

      });
}
function importmarks(){
    $("#btn-import-marks").change(function(e){
          swal({
              title: "Importing...",
              imageUrl: spinner,
              showConfirmButton: false,
              allowOutsideClick: false
            });
			var selectedFile= e.target.files[0];
			 var data = new FormData();
            data.append('file', selectedFile);
            var url = 'importmarks';
            $.ajax({
                type: 'POST',
                url: url,
                data: data,
                processData: false,
                contentType: false

            }).done(function (s) {
                 swal.close();
                 swal({
                    type: 'success',
                    title: 'Success',
                    text: s.success,
                    showConfirmButton: true
                })
                $('#btn-import-marks').val('');
		    getExamMarks($('#regCode').val())
            $('#marks').val('')
            $('#examRemarks').val('')
            $('#examPercentageMarks').val('')
            $('#displayGrade').val('')

            }).fail(function (xhr, error) {
                 swal.close();
                 $('#btn-import-marks').val('');

		        getExamMarks($('#regCode').val())
                p=JSON.parse(xhr.responseText)

                console.log(p.error)

                    bootbox.alert(p.error)

                // bootbox.alert("Error Occured while saving")
            })

        })
}
function downloadmarks(){
    $("#downloadmarks").click(function(e){
            var url = 'downloadmarks';
            $.ajax({
                type: 'GET',
                url: url

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
function classChange() {
    $('#class_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#classCode').val(data.id)
        $('#examExcelClass').val(data.id)
     searchTeacher();
    });
    $("#class_frm").on("select2:unselecting", function(e) {
    $('#classCode').val('')
 });
}
function searchExam(term,year) {
       $('#reg_frm').select2({
            placeholder: 'Exam',
            allowClear: true,
                        width: '67%',

            ajax: {
                delay: 250,
                url: 'searchexamregister/'+term+'/'+year,
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

function termChange() {
    $('#term_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#termCode').val(data.id)
         $('#termName').val('T'+data.text+'_')
        $('#examName').val($('#termName').val()+$('#monthName').val()+$('#yearName').val()+$('#typeName').val())
         searchYear()
        if($('#yearCode').val()!==''){
            $('#reg_frm').empty()
            $('#regCode').val('')
            searchExam(data.id,$('#yearCode').val());
        }
    });
    $("#term_frm").on("select2:unselecting", function(e) {
    $('#termCode').val('')
    $('#termName').val('')

 });
}

function getGrading(id) {
   $.ajax({
			type: 'GET',
			url: 'getgradingscheme/'+id,
		}).done(function (s) {
		     if (s.gradeCode) {
                $('#gradeCode').val(s.gradeCode)
                var $newCode = $("<option selected='selected' value='" + s.gradeCode + "'>'+s.gradeName+'</option>").val(s.gradeCode.toString()).text(s.gradeName)
                $('#grading_frm').append($newCode).trigger('change');
            }
            else {
                $('#gradeCode').val('')
                $('#grading_frm').empty();
            }
		}).fail(function (xhr, error) {
						bootbox.alert('No Grading Scheme set for this exam!')
            // bootbox.alert("Error Occured while saving")
		})
}

function examChange() {
    $('#reg_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#regCode').val(data.id)
        $('#examExcelCode').val(data.id)
        getExamMarks(data.id)
        searchClass()
        getGrading(data.id)
    });
    $("#reg_frm").on("select2:unselecting", function(e) {
    $('#regCode').val('')
     $('#gradeCode').val('')
     $('#grading_frm').empty();

 });
}
function editMarks(){
    $('#processTable').on('click','.btn-editexam',function (s) {
        var data=$(this).closest('tr').find('#edit-exam').val();
        $.ajax({
            type: 'GET',
            url: 'editmarks/'+data,
        }).done(function (s) {
            $('#processCode').val(s[0].processCode)
            $('#examRemarks').val(s[0].remarks);
            $('#examDate').val(s[0].examDate);
            $('#marks').val(s[0].marks);
            $('#outof').val(s[0].outof);
            $('#displayGrade').val(s[0].grade);
            $('#processGrade').val(s[0].grade);
            $('#userLogged').val(s[0].user)

             if (s[0].termCode) {
                $('#termCode').val(s[0].termCode)
                var $newTerm = $("<option selected='selected' value='" + s[0].termCode + "'>'+s[0].termNumber+'</option>").val(s[0].termCode.toString()).text(s[0].termNumber)
                $('#term_frm').append($newTerm).trigger('change');
                searchYear()
            }
            else {
                $('#termCode').val('')
                $('#term_frm').empty();
            }
               if (s[0].yearCode) {
                $('#yearCode').val(s[0].yearCode)
                var $newYear = $("<option selected='selected' value='" + s[0].yearCode + "'>'+s[0].yearNumber+'</option>").val(s[0].yearCode.toString()).text(s[0].yearNumber)
                $('#year_frm').append($newYear).trigger('change');
                searchExam($('#termCode').val(),s[0].yearCode)
            }
            else {
                $('#yearCode').val('')
                $('#year_frm').empty();
            }

               if (s[0].examCode) {
                $('#regCode').val(s[0].examCode)
                                   $('#examExcelCode').val(s[0].examCode)

                var $newCode = $("<option selected='selected' value='" + s[0].examCode + "'>'+s[0].examName+'</option>").val(s[0].examCode.toString()).text(s[0].examName)
                $('#reg_frm').append($newCode).trigger('change');
                searchClass();
                getGrading(s[0].examCode)
            }
            else {
                $('#regCode').val('')
                $('#reg_frm').empty();
                $('#gradeCode').val('')
                $('#grading_frm').empty()
                   $('#examExcelCode').val('')

            }
            if (s[0].classCode) {
			    var $newCl = $("<option selected='selected' value='" + s[0].classCode + "'>'+s[0].className+'</option>").val(s[0].classCode.toString()).text(s[0].className)

                $('#class_frm').append($newCl).trigger('change');
			    $('#classCode').val(s[0].classCode)
                			    $('#examExcelClass').val(s[0].classCode)

                searchTeacher();
			    }
			    else {
			    $('#class_frm').empty();
			    $('#classCode').val('')
                $('#examExcelClass').val('')

			}
			     if (s[0].teacherCode) {

                $('#teacherCode').val(s[0].teacherCode)
               $('#examExcelTeacher').val(s[0].teacherCode)
                var $newOption = $("<option selected='selected' value='" + s[0].teacherCode + "'>'+s[0].teacherName+'</option>").val(s[0].teacherCode.toString()).text(s[0].teacherName)

                $('#teacher_frm').append($newOption).trigger('change');
                searchSubjects($('#classCode').val(),s[0].teacherCode)
            } else {
                $('#teacherCode').val('')
               $('#examExcelTeacher').val('')

                $('#teacher_frm').empty();

            }
			       if (s[0].subjectCode) {
                $('#subjectCode').val(s[0].subjectCode)
                $('#examExcelSubject').val(s[0].subjectCode)

                var $newOption = $("<option selected='selected' value='" + s[0].subjectCode + "'>'+s[0].subjectName+'</option>").val(s[0].subjectCode.toString()).text(s[0].subjectName)

                $('#subject_frm').append($newOption).trigger('change');
                $('#exportBtn').prop('disabled',false)

                searchStudent($('#classCode').val(),s[0].subjectCode)
            } else {
                $('#subjectCode').val('')
                $('#examExcelSubject').val('')
                $('#subject_frm').empty();
                                $('#exportBtn').prop('disabled',true)


            }
			         if (s[0].studentCode) {
                $('#studentCode').val(s[0].studentCode)

                var $newOption = $("<option selected='selected' value='" + s[0].studentCode + "'>'+s[0].studentName+'</option>").val(s[0].studentCode.toString()).text(s[0].studentName)

                $('#student_frm').append($newOption).trigger('change');
            } else {
                $('#studentCode').val('')

                $('#student_frm').empty();

            }


        }).fail(function (xhr, error) {
        bootbox.alert(xhr.responseText)
        });
    });

}
function getExamMarks(id) {
    console.log(id)
    url=''
    if(id === undefined || id === ''){
        url='getrecordedmarks'
    }
    else{
        url='getexamrecordedmarks/'+id
    }
        $.ajax({
        type: 'GET',
        url: url,
    }).done(function (s) {

   $('#processTable').DataTable().destroy();
        $("#processTable tbody").empty();
        $.each(s,function(i,item){
            $("#processTable tbody").append(
                "<tr>"
                +"<td>"+item.name+"</td>"
                +"<td>"+item.admNo+"</td>"
                +"<td>"+item.subject+"</td>"
               +"<td>"+item.examName+"</td>"
                +"<td>"+item.marks+"</td>"
                +"<td>"+item.outof+"</td>"
                +"<td>"+item.percentage+"</td>"
                +"<td>"+item.grade+"</td>"

                +"<td>"+item.term+"</td>"
                +"<td>"+item.year+"</td>"
                 +"<td>"+item.teacher+"</td>"
                 +"<td>"+item.className+"</td>"
                +"<td>"+item.remarks+"</td>"
                +"<td>"+item.examDate+"</td>"
                +"<td>"+item.user+"</td>"
                +"<td>"+'<form id="editForm" method="post" enctype="multipart/form-data"><input type="hidden" id="edit-exam" name="id" value='+item.processCode+'></form><button class="btn btn-outline-primary btn-sm btn-editexam" ><i class="fa fa-edit"></button>'
                +"</td>"
                +"<td>"+'<form id="deleteForm" method="post" enctype="multipart/form-data"><input type="hidden" id="delete-exam" name="id" value='+item.processCode+'></form><button class="btn btn-outline-danger btn-sm btn-deleteexam" ><i class="fa fa-trash-o"></button>'
                +"</tr>" )
         })
        $('#processTable').DataTable();
    }).fail(function (xhr, error) {
       bootbox.alert(xhr.responseText);
    });


}

function saveMarks(){
     $('#saveMarks').click(function () {
        var data=$('#processing-form').serialize();
        var url = '';
        if($('#processCode').val()===''){
          url = 'saveexammarks'
        }else{
            url = 'updateexammarks/'+$('#processCode').val()
        }
        if($('#examRemarks').val()==='' || $('#gradeCode').val()===''){
              swal({
          title: 'Alert!',
          type: 'info',
          text: 'Grade and Remarks are mandatory'
      })
        }
        else{
		$.ajax({
			type: 'POST',
			url: url,
            data: data
		}).done(function (s) {
		     swal({
                    type: 'success',
                    title: 'Success',
                    text: s.success,
                    showConfirmButton: true
                })
		    getExamMarks($('#regCode').val());
            $('#marks').val('')
            $('#examRemarks').val('')
            $('#examPercentageMarks').val('')
            $('#displayGrade').val('')


		}).fail(function (xhr, error) {
						bootbox.alert(xhr.responseText)
            // bootbox.alert("Error Occured while saving")
		})

}
	})

}
function deleteMarks() {
     $('#processTable').on('click','.btn-deleteexam',function (s) {
        var data = $(this).closest('tr').find('#delete-exam').val();
        bootbox.confirm("Are you sure want to delete this Exam Marks?", function (result) {
            if (result) {
               $.ajax({
            type: 'GET',
            url: 'deleteexammarks/'+data,

        }).done(function (s) {
          getExamMarks($('#regCode').val())
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
function calculateMarks(){
  $('#marks').on('input',function () {
         var outof = $('#outof').val();
          var marks = $('#marks').val();
          var scheme = $('#gradeCode').val();

      if($('#outof').val() === ''){
         bootbox.alert('Provide Out of field First');
      }
      else {


          if (marks === '' || outof === '' || scheme === '') {
              bootbox.alert('Either marks or out of or grading scheme is missing');

          } else {
             console.log('marks '+marks+' '+'outof '+outof)

      if(parseInt(outof) < parseInt(marks)){
                 bootbox.alert('Marks cannot be greater than out of value');

      }
      else {
          $.ajax({
              type: 'GET',
              url: 'processgrade',
              data: {
                  marks: marks,
                  outof: outof,
                  scheme: scheme

              }
          }).done(function (s) {
              $('#processGrade').val(s[0].grade)
              $('#displayGrade').val(s[0].grade)
              $('#examPercentageMarks').val(s[0].results)
              $('#examRemarks').val(s[0].remarks)

          }).fail(function (xhr, error) {
              bootbox.alert(xhr.responseText)
          })
      }
          }
      }
  })
}