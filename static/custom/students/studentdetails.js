

$(document).ready(function () {
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        }
    });
formatDate();
searchClass();
classChange();
searchParent();
parentChange();
searchFeeCategory();
feeChange();
studentImage("");
searchDorm();
dormChange();
searchCampus();
campusChange();
searchNationality();
countryChange();
countyChange();
subCountyChange();
locationChange();
subLocationChange();
villageChange();
searchDenomination();
denominationChange();
searchSources();
sourcesChange();
searchYear();
yearChange();
searchHealth();
searchStatus();
statusChange();
healthChange();
searchDocument();
documentChange();
})
function studentImage(url){
        $("#student-avatar").fileinput('destroy').fileinput({
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
function formatDate() {
    var d = new Date(),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2)
        month = '0' + month;
    if (day.length < 2)
        day = '0' + day;

    $('#dob').val([year, month, day].join('-'))
    $('#completionDate').val([year, month, day].join('-'))
    $('#admDate').val([year, month, day].join('-'))

}

function searchClass() {
        $('#class_frm').select2({
            placeholder: 'Class Admitted',
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
function searchParent() {
     $('#parent_frm').select2({
           placeholder: 'Names',
           allowClear: true,
           ajax: {
             delay: 250,
             url: 'searchparent',
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
function searchDocument() {
     $('#document_frm').select2({
           placeholder: 'Document',
           allowClear: true,
           width: '50%' ,

           ajax: {
             delay: 250,
             url: 'searchdocs',
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

function searchFeeCategory() {
     $('#fee_frm').select2({
           placeholder: 'Fees',
           allowClear: true,
           ajax: {
             delay: 250,
             url: 'searchfeecategory',
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

function searchDorm() {
        $('#dorm_frm').select2({
            placeholder: 'House',
            allowClear: true,
            ajax: {
                delay: 250,
                url: 'searchdorms',
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
function searchCampus() {
     $('#campus_frm').select2({
           placeholder: 'Campus',
           allowClear: true,
           ajax: {
             delay: 250,
             url: 'searchcampus',
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
function countryChange() {
    $('#nationality_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#nationality').val(data.id)

        // console.log('country is: '+$('#country-id').val())
        searchCounties(data.id)

    });
    $("#nationality_frm").on("select2:unselecting", function(e) {
    $('#nationality').val('')
 });
}
function documentChange() {
    $('#document_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#studentDocument').val(data.id)

        // console.log('country is: '+$('#country-id').val())

    });
    $("#document_frm").on("select2:unselecting", function(e) {
    $('#studentDocument').val('')
 });
}
function classChange() {
    $('#class_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#studentClass').val(data.id)

        // console.log('country is: '+$('#country-id').val())

    });
    $("#class_frm").on("select2:unselecting", function(e) {
    $('#studentClass').val('')
 });
}
function campusChange() {
    $('#campus_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#campus').val(data.id)

        // console.log('country is: '+$('#country-id').val())

    });
    $("#campus_frm").on("select2:unselecting", function(e) {
    $('#campus').val('')
 });
}
function feeChange() {
    $('#fee_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#feeCategory').val(data.id)

        // console.log('country is: '+$('#country-id').val())

    });
    $("#fee_frm").on("select2:unselecting", function(e) {
    $('#feeCategory').val('')
 });
}
function parentChange() {
    $('#parent_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#parent').val(data.id)

        // console.log('country is: '+$('#country-id').val())

    });
    $("#parent_frm").on("select2:unselecting", function(e) {
    $('#parent').val('')
 });
}
function dormChange() {
    $('#dorm_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#dorm').val(data.id)

        // console.log('country is: '+$('#country-id').val())

    });
    $("#dorm_frm").on("select2:unselecting", function(e) {
    $('#dorm').val('')
 });
}
function countyChange() {
    $('#county_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#studentCounty').val(data.id)

        // console.log('country is: '+$('#country-id').val())
        searchSubCounty(data.id)

    });
    $("#county_frm").on("select2:unselecting", function(e) {
    $('#studentCounty').val('')
 });
}
function subLocationChange() {
   $('#sublocation_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#subLocation').val(data.id)

        // console.log('country is: '+$('#country-id').val())
        searchVillage(data.id)

    });
    $("#sublocation_frm").on("select2:unselecting", function(e) {
    $('#subLocation').val('')
 });
}
function villageChange() {
   $('#village_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#village').val(data.id)

        // console.log('country is: '+$('#country-id').val())

    });
    $("#village_frm").on("select2:unselecting", function(e) {
    $('#village').val('')
 });
}
function denominationChange() {
   $('#denomination_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#religion').val(data.id)

        // console.log('country is: '+$('#country-id').val())

    });
    $("#denomination_frm").on("select2:unselecting", function(e) {
    $('#religion').val('')
 });
}
function sourcesChange() {
   $('#sources_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#sources').val(data.id)

        // console.log('country is: '+$('#country-id').val())

    });
    $("#sources_frm").on("select2:unselecting", function(e) {
    $('#sources').val('')
 });
}
function subCountyChange() {
    $('#subcounty_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#subCounty').val(data.id)

        // console.log('country is: '+$('#country-id').val())
        searchLocation(data.id)

    });
    $("#subcounty_frm").on("select2:unselecting", function(e) {
    $('#subCounty').val('')
 });
}
function locationChange() {
    $('#location_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#location').val(data.id)

        // console.log('country is: '+$('#country-id').val())
        searchSubLocation(data.id)

    });
    $("#location_frm").on("select2:unselecting", function(e) {
    $('#location').val('')
 });
}
function yearChange() {
    $('#year_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#year').val(data.id)
    });
    $("#year_frm").on("select2:unselecting", function(e) {
    $('#year').val('')
 });
}
function healthChange() {
    $('#healthstatus_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#healthStatus').val(data.id)
    });
    $("#healthstatus_frm").on("select2:unselecting", function(e) {
    $('#healthStatus').val('')
 });
}
function statusChange() {
    $('#studentstatus_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#studentStatus').val(data.id)
    });
    $("#studentstatus_frm").on("select2:unselecting", function(e) {
    $('#studentStatus').val('')
 });
}
function searchNationality() {
        $('#nationality_frm').select2({
            placeholder: 'Countries',
            allowClear: true,
            width: '50%' ,
            ajax: {
                delay: 250,
                url: 'searchcountry',
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
function searchDenomination() {
        $('#denomination_frm').select2({
            placeholder: 'Denomination',
            allowClear: true,
            width: '50%' ,
            ajax: {
                delay: 250,
                url: 'searchdenominations',
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
function searchSources() {
        $('#sources_frm').select2({
            placeholder: 'Sources',
            allowClear: true,
            width: '50%' ,
            ajax: {
                delay: 250,
                url: 'searchstudentsources',
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
function searchYear() {
        $('#year_frm').select2({
            placeholder: 'Year',
            allowClear: true,
            width: '15%' ,
            ajax: {
                delay: 250,
                url: 'searchyears',
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
function searchHealth() {
        $('#healthstatus_frm').select2({
            placeholder: 'Conditions',
            allowClear: true,
            width: '50%' ,
            ajax: {
                delay: 250,
                url: 'searchhealthstatus',
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
function searchStatus() {
        $('#studentstatus_frm').select2({
            placeholder: 'Status',
            allowClear: true,
            width: '50%' ,
            ajax: {
                delay: 250,
                url: 'searchstudentstatus',
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
function searchSubCounty(id) {
        $('#subcounty_frm').select2({
            placeholder: 'SubCounty',
            allowClear: true,
            width: '50%' ,
            ajax: {
                delay: 250,
                url: 'searchsubcounty/'+id,
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
function searchCounties(id) {

     $('#county_frm').select2({
           placeholder: 'Counties',
           allowClear: true,
           width: '50%' ,
           ajax: {
             delay: 250,
             url: 'searchcounties/'+id,
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
function searchLocation(id) {

     $('#location_frm').select2({
           placeholder: 'Location',
           allowClear: true,
           width: '50%' ,
           ajax: {
             delay: 250,
             url: 'searchlocation/'+id,
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
function searchSubLocation(id) {

     $('#sublocation_frm').select2({
           placeholder: 'SubLocation',
           allowClear: true,
           width: '50%' ,
           ajax: {
             delay: 250,
             url: 'searchsublocation/'+id,
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
function searchVillage(id) {

     $('#village_frm').select2({
           placeholder: 'Village',
           allowClear: true,
           width: '50%' ,
           ajax: {
             delay: 250,
             url: 'searchvillage/'+id,
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