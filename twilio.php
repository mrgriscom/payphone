<?php echo '<?xml version="1.0" encoding="utf-8" ?>' ?>
<Response>
  <Dial callerId="+[twilio origin number, eg. 15556667777]">
    <Number><? preg_match('/:([0-9]+)@/', $_POST['To'], $matches); echo $matches[1]; ?></Number>
  </Dial>
</Response>

