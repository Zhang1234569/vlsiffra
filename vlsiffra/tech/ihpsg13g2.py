from amaranth import Elaboratable, Instance, Signal


class IHPSG13G2Process(Elaboratable):
    def _PoweredInstance(self, *args, **kwargs):
        # The open IHP SG13G2 Verilog models do not expose power pins.
        return Instance(*args, **kwargs)

    def _add_submodule(self, instance, name=None):
        if name:
            self.m.submodules[name] = instance
        else:
            self.m.submodules += instance

    def _generate_and(self, a, b, o, name=None):
        andgate = self._PoweredInstance(
            "sg13g2_and2_1",
            i_A=a,
            i_B=b,
            o_X=o
        )

        self._add_submodule(andgate, name)

    def _generate_xor(self, a, b, o, name=None):
        xorgate = self._PoweredInstance(
            "sg13g2_xor2_1",
            i_A=a,
            i_B=b,
            o_X=o
        )

        self._add_submodule(xorgate, name)

    def _generate_inv(self, a, o, name=None):
        invgate = self._PoweredInstance(
            "sg13g2_inv_1",
            i_A=a,
            o_Y=o
        )

        self._add_submodule(invgate, name)

    def _generate_full_adder(self, a, b, carry_in, sum_out, carry_out, name=None):
        p = Signal()
        g = Signal()

        self._generate_xor(a, b, p, name)
        self._generate_xor(p, carry_in, sum_out)
        self._generate_and(a, b, g)
        self._generate_ao21(p, carry_in, g, carry_out)

    def _generate_half_adder(self, a, b, sum_out, carry_out, name=None):
        self._generate_xor(a, b, sum_out, name)
        self._generate_and(a, b, carry_out)

    # Used in adder
    def _generate_ao21(self, a1, a2, b1, o):
        """ 2-input AND into first input of 2-input OR. """
        a21o = self._PoweredInstance(
            "sg13g2_a21o_1",
            i_A1=a1,
            i_A2=a2,
            i_B1=b1,
            o_X=o
        )

        self.m.submodules += a21o

    # Used in multiplier
    def _generate_ao22(self, a1, a2, b1, b2, o):
        """ 2-input AND into both inputs of 2-input OR. """
        zn = Signal()

        a22oi = self._PoweredInstance(
            "sg13g2_a22oi_1",
            i_A1=a1,
            i_A2=a2,
            i_B1=b1,
            i_B2=b2,
            o_Y=zn
        )
        self.m.submodules += a22oi

        self._generate_inv(zn, o)

    # Used in multiplier
    def _generate_ao32(self, a1, a2, a3, b1, b2, o):
        """ 3-input AND into first input, and 2-input AND into 2nd input of 2-input OR. """
        a12 = Signal()
        a123 = Signal()

        self._generate_and(a1, a2, a12)
        self._generate_and(a12, a3, a123)
        self._generate_ao21(b1, b2, a123, o)
