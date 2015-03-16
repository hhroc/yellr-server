'use strict';

angular
    .module('Yellr')
    .directive('pwCheck', [function () {
        return {
            require: 'ngModel',
            link: function (scope, elem, attr, ctrl) {
                var firstPassword = '#' + attr.pwCheck;
                elem.add(firstPassword).on('keyup', function () {
                    scope.$apply(function () {
                        ctrl.$setValidity('pwMatch',
                            elem.val() === $(firstPassword).val());
                    });
                });
            }
        };
    }]);
