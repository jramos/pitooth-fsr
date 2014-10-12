#include <stdio.h>
#include <fcntl.h>
#include <linux/input.h>
#include <sstream>

#define EV_PRESSED 1
#define EV_RELEASED 0
#define EV_REPEAT 2

main() 
{
  int fd = 0;
  char *device = "/dev/input/event0";

  // Write a key to the keyboard buffer
  if( (fd = open(device, O_RDWR)) > 0 )
  {
    struct input_event event;

    // Press a key
    event.type = EV_KEY;
    event.value = EV_PRESSED;
    event.code = KEY_S;
    write(fd, &event, sizeof(struct input_event) * 4);

    // Release the key
    event.value = EV_RELEASED;
    event.code = KEY_S;
    write(fd, &event, sizeof(struct input_event) * 4);

    close(fd);
  }
}
