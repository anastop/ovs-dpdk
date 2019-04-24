apt install -y python3-pip
pip3 install qemu-affinity


ps -C qemu-system-x86 -o pid=
(Outputs each PID on a separate line)

grp 

qemu-affinity -k 2:${cpu_vm1_core2} -- 54844
qemu-affinity -k 3:${cpu_vm1_core3} -- 54844

qemu-affinity -p *:${cpu_vm2_core0},${cpu_vm2_core1} -w *:${cpu_vm2_core0},${cpu_vm2_core1}  -i *:${cpu_vm2_core0},${cpu_vm2_core1} -q *:${cpu_vm2_core0},${cpu_vm2_core1} -k 2:${cpu_vm1_core2} 3:${cpu_vm1_core3} *:${cpu_vm2_core0},${cpu_vm2_core1}  -- 54845



qemu-affinity -p ${cpu_vm1_core0},${cpu_vm1_core1} -k 2:${cpu_vm1_core2} 3:${cpu_vm1_core3} -- 54844


>>> x = 0b10001000
You can find out whether the top bits are set with:

>>> bit8 = bool(x & 0b10000000)
>>> bit7 = bool(x & 0b01000000)
To find which lower bit is set, use a dictionary:

>>> bdict = dict((1<<i, i+1) for i in range(6))
>>> bdict[x & 0b00111111]
4


To hex string. Note that you don't need to use x8 bits.


Toggle line numbers
   1 >>> print "0x%x" % int('11111111', 2)
   2 0xff
   3 >>> print "0x%x" % int('0110110110', 2)
   4 0x1b6
   5 >>> print "0x%x" % int('0010101110101100111010101101010111110101010101', 2)
   6 0xaeb3ab57d55