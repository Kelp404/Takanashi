// Generated by CoffeeScript 1.6.3
(function() {
  var v;

  v = angular.module('victory.directive', []);

  v.directive('vTooltip', function() {
    /*
    Show the bootstrap tool tip.
    */

    return function(scope, element, attrs) {
      if (attrs.vTooltip) {
        $(element).attr('title', scope.$eval(attrs.vTooltip));
      }
      return $(element).tooltip();
    };
  });

  v.directive('vFocus', function() {
    /*
    Focus this element.
    */

    return function(scope, element, attrs) {
      return $(element).select();
    };
  });

  v.directive('vModal', function() {
    /*
    Find the first input text box then focus it on the bootstrap modal window.
    */

    return function(scope, element, attrs) {
      return $(element).on('shown', function() {
        return $(this).find('input:first').select();
      });
    };
  });

  v.directive('vEnter', function() {
    /*
    Eval the AngularJS expression when pressed `Enter`.
    */

    return function(scope, element, attrs) {
      return element.bind("keydown keypress", function(event) {
        if (event.which === 13) {
          scope.$apply(function() {
            return scope.$eval(attrs.vEnter);
          });
          return event.preventDefault();
        }
      });
    };
  });

  v.directive('vNavigation', function() {
    /*
    Setup the navigation effect.
    */

    return function(scope, element, attrs) {
      var $selected, index, match, noop;
      if ($(element).find('li.select').length > 0) {
        $selected = $(element).find('li.select');
      } else {
        match = location.href.match(/\w\/([/#\w]*)/);
        index = match[1] === '' ? 0 : $(element).find('li a[href*="' + match[1] + '"]').parent().index();
        $selected = $(element).find('li').eq(index);
      }
      $(element).find('li:first').parent().prepend($('<li class="cs_top"></li>'));
      $(element).find('li.cs_top').css({
        width: $selected.css('width'),
        left: $selected.position().left,
        top: $selected.position().top
      });
      noop = function() {};
      $(element).find('li[class!=cs_top]').hover(function() {
        return $(element).find('li.cs_top').each(function() {
          return $(this).dequeue();
        }).animate({
          width: this.offsetWidth,
          left: this.offsetLeft
        }, 420, "easeInOutCubic");
      }, noop());
      $(element).hover(noop(), function() {
        return $(element).find('li.cs_top').each(function() {
          return $(this).dequeue();
        }).animate({
          width: $(element).find('li.select').css('width'),
          left: $(element).find('li.select').position().left
        }, 420, "easeInOutCubic");
      });
    };
  });

}).call(this);
