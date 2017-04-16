'use strict';

/*global $:false */

var FormSet = function(form, prefix) {
  this.$form = $(form);
  this.prefix = prefix || 'form';
  this.regex = new RegExp('(' + this.prefix + '-\\d+-)');
};

FormSet.prototype.updateElementIndex = function (el, ndx) {
  var replacement = this.prefix + '-' + ndx + '-',
      element = $(el),
      attrs = ['for', 'id', 'name', 'data-component-target', 'data-component-name', 'data-prefix'];

  attrs.forEach(function(attr) {
    var attrValue = el.attr(attr);
    if (attrValue) {
      el.attr(attr, attrValue.replace(this.regex, replacement));
    }
  }.bind(this));
};

FormSet.prototype.count = function(count) {
  var key = '#id_' + this.prefix + '-TOTAL_FORMS';
  var el = $(key);

  if (count === undefined) {
    return parseInt(el.val(), 10);
  }

  el.val(count);
};

FormSet.prototype.remove = function(btn, callback) {
  var formCount = this.count();

  if (formCount < 1) {
    return;
  }

  var parent = $(btn).parents('.item:first');
  var hidden = parent.find('input[type=checkbox][name*="DELETE"]');
  var i = 0;
  var _this = this;

  if (hidden.length) {
    hidden.prop('checked', true);
    parent.hide();
  } else {
    parent.remove();

    var forms = this.$form.find('.item');

    this.count(forms.length);

    var updateElementIndex = function() {
      if ($(this).attr('type') === 'text') {
        _this.updateElementIndex(this, i);
      }
    };

    for (formCount = forms.length; i < formCount; i++) {
      $(forms.get(i)).children().children().each(updateElementIndex);
    }

    if (callback !== undefined) {
      callback(forms);
    }
  }
};

FormSet.prototype.add = function () {
  var formCount = this.count(),
      last = this.$form.find('.item:last'),
      row = last.clone(false).get(0),
      _this = this;

  $(row).removeAttr('id').hide().insertAfter(last).slideDown(300);

  $('.errorlist', row).remove();


  $(row).find('input,textarea,select,label,[data-component="tab"],div[id^="tab-content"],.js-contrib-tabs').each(function () {
    _this.updateElementIndex($(this), formCount);
    $(this).val('');
  });

  $(row).find('.delete').click(function() {
    return _this.remove($(this));
  });

  _this.count(formCount + 1);

  return row;
};

$.fn.FormSet = function() {
  return this.each(function() {
    var $this = $(this);
    var data = $this.data('formset');

    if (!data) {
      $this.data('FormSet', new FormSet(this, $this.data.get('prefix')));
    }
  });
};

$.fn.FormSet.Constructor = FormSet;
