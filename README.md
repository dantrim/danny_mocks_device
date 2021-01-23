# danny_mocks_device
Playing around with how to setup mock serial devices for testing of lab equipment software

# Goal
Rely on pseudo-terminals to provide OS pipes/file descriptors that can respond
to commands that we typically send to actual hardware.
The idea here is not to provide a fully functional emulation of hardware, but
to at least mock the behavior (e.g. a certain command expects a reply, and that reply
should be a positive number -- the actual values are not relevant).
Running a mock device on a thread which is monitoring the OS pipe, we can
define specific "command suite handlers", e.g. for the SCPI command suite, such
that it can generate behaviorally correct responses to send back through
the file descriptor.

# References/Inspiration
A lot of the idea for this, at least for how to register handlers properly
and somewhat generically, is from [pyvisa-mock](https://github.com/microsoft/pyvisa-mock)
(specifically it's [mock SCPI handler](https://github.com/microsoft/pyvisa-mock/blob/9c8fb8efc7740fcbfb3293fedafe9c4066ba7ee5/visa_mock/base/base_mocker.py#L36)).
