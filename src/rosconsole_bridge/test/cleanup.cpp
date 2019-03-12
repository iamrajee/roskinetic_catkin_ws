#include <console_bridge/console.h>
#include <rosconsole_bridge/bridge.h>

// Remove this when no longer supporting platforms with libconsole-bridge-dev < 0.3.0,
// in particular Debian Jessie: https://packages.debian.org/jessie/libconsole-bridge-dev
#ifndef CONSOLE_BRIDGE_logWarn
  #define CONSOLE_BRIDGE_logWarn logWarn
#endif

struct A {
  A(const char* hint) {
    CONSOLE_BRIDGE_logWarn("initializing class: %s", hint);
  }
  ~A() {
    CONSOLE_BRIDGE_logWarn("destroying class");
  }
};

// destructor of static instance should use the original output handler
static A a("static");

REGISTER_ROSCONSOLE_BRIDGE;

int main(int argc, char **argv)
{
  A a("local");
  return 0;
}
