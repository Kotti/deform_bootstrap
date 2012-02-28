
deform.appendSequenceItem = (node) ->
    $oid_node = $(node).parent()
    $proto_node = $oid_node.children('.deformProto')
                           .first()
    $before_node = $oid_node.children('.deformSeqContainer')
                            .first()
                            .children('.deformInsertBefore')
    min_len = parseInt($before_node.attr('min_len')||'0')
    max_len = parseInt($before_node.attr('max_len')||'9999')
    now_len = parseInt($before_node.attr('now_len')||'0')
    if now_len < max_len
        deform.addSequenceItem($proto_node, $before_node)
        deform.processSequenceButtons($oid_node, min_len, max_len, now_len+1)
    false

deform.processSequenceButtons = (oid_node, min_len, max_len, now_len) ->
    $ul = oid_node.children('.deformSeqContainer')
    $lis = $ul.children('.deformSeqItem')
    $lis.find('.deformClosebutton')
        .removeClass('deformClosebuttonActive')
    oid_node.children('.deformSeqAdd')
            .show()
    if now_len > min_len
        $lis.find('.deformClosebutton')
            .addClass('deformClosebuttonActive')
    if now_len >= max_len
        oid_node.children('.deformSeqAdd')
                .hide()
