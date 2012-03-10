/*jslint undef: true */
/*global $: false, deform: false */

(function() {

  deform.appendSequenceItem = function(node) {
    var $before_node, $oid_node, $proto_node, max_len, min_len, now_len;
    $oid_node = $(node).parent();
    $proto_node = $oid_node.children('.deformProto').first();
    $before_node = $oid_node.children('.deformSeqContainer').first().children('.deformInsertBefore');
    min_len = parseInt($before_node.attr('min_len') || '0', 10);
    max_len = parseInt($before_node.attr('max_len') || '9999', 10);
    now_len = parseInt($before_node.attr('now_len') || '0', 10);
    if (now_len < max_len) {
      deform.addSequenceItem($proto_node, $before_node);
      deform.processSequenceButtons($oid_node, min_len, max_len, now_len + 1);
    }
    return false;
  };

  deform.processSequenceButtons = function(oid_node, min_len, max_len, now_len) {
    var $lis, $ul;
    $ul = oid_node.children('.deformSeqContainer');
    $lis = $ul.children('.deformSeqItem');

    $lis.children('.close').toggle(now_len > min_len);
    oid_node.children('.deformSeqAdd').toggle(now_len < max_len);
  };

}.call(this));
