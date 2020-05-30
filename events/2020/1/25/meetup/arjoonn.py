from slideshow import slideshow
from textwrap import dedent

slide, run = slideshow(fail_silent=False)


@slide
def ssh():
    return "SSH: koi hai"


@slide
def outline():
    return dedent(
        """\
    SSH
    ===

    1. Intro
        - Connecting
        - Running commands
    2. Applications
        - Chat
        - Getting access to blocked services
        - Transferring files
    3. Shaktimaan mode
        - That movie scene where calls are traced
        - Accessing machines from anywhere
    4. Wrapup
    """
    )


@slide
def intro():
    return dedent(
        """\
    Connecting
    ==========

    ssh pyj@mumbai.arjoonn.com
    """
    )


@slide
def running_commands():
    return dedent(
        """\
    Running commands
    ================

    ssh pyj@mumbai.arjoonn.com ls
    """
    )


@slide
def chat():
    return dedent(
        """\
    Chat
    ====

    ssh pyj@mumbai.arjoonn.com
    wall 'Hi! Arjoonn here'
    """
    )


@slide
def sock_proxy():
    return dedent(
        """\
    Proxy
    =====

    ssh -D 9999 pyj@mumbai.arjoonn.com
    """
    )


@slide
def file_transfers():
    return dedent(
        """\
    Proxy
    =====

    scp ~/arjoonn/movie.mp4 pyj@mumbai.arjoonn.com:~/arjoonn
    """
    )


@slide
def ssh_chaining():
    return dedent(
        """\
    SSh Chains
    =====

    ssh1: ssh pyj@mumbai.arjoonn.com
    ssh2: ssh pyj@singapore.arjoonn.com

                 mumbai     singapore  
                +-------+  +---------+
                |       |  |         |
                |       |  |         |
    ssh 1 ======> ssh 2 ===>         |
                |       |  |         |
                |       |  |         |
                +-------+  +---------+
    """
    )


@slide
def port_tunnels_local():
    return dedent(
        """\
    Tunnels: Local -> Remote
    =======

    ssh -L 8080:localhost:8080 pyj@mumbai.arjoonn.com
    """
    )


@slide
def port_tunnels_remote():
    return dedent(
        """\
    Tunnels: Access any machine from anywhere
    =======

    Home        : ssh -R 22222:localhost:22 pyj@mumbai.arjoonn.com
    Laptop      : ssh pyj@mumbai.arjoonn.com
    Common      : ssh -p 22222 arjoonn@localhost
    """
    )


@slide
def thanks():
    return dedent(
        """\
    arjoonn.com
    ===========

    t.me/arjoonn
    twitter.com/arjoonn1
    github.com/thesage21
    gitlab.com/thesage21
    """
    )


ss = run()
next(ss)
