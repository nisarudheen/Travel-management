odoo.define('travels_management.web_location_slot', function (require) {
'use strict';

var core = require('web.core');
var publicWidget = require('web.public.widget');
var qweb = core.qweb;
var rpc = require('web.rpc');


publicWidget.registry.NewClass= publicWidget.Widget.extend({
    selector: '.values',
    events:{
    'change #from_location':'_onchange_from_location',

    },
    _onchange_from_location:function(){
        var location = document.getElementById("from_location").value;
        console.log(location)
        rpc.query({
                route: "/booking/location",
                params: {
                    location:location
                    },
                }).then(function (list) {
        var select = document.querySelector('#to_location');
        for (let i = 0; i < list.length; i++) {
           let option =new Option(list[i], list[i]);
           select.add(option);
        }

        })
            },
            });
            });