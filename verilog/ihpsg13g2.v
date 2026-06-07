module sg13g2_and2_1 (X, A, B);
    output X;
    input A, B;

    assign X = A & B;
endmodule

module sg13g2_xor2_1 (X, A, B);
    output X;
    input A, B;

    assign X = A ^ B;
endmodule

module sg13g2_inv_1 (Y, A);
    output Y;
    input A;

    assign Y = ~A;
endmodule

module sg13g2_a21o_1 (X, A1, A2, B1);
    output X;
    input A1, A2, B1;

    assign X = (A1 & A2) | B1;
endmodule

module sg13g2_a22oi_1 (Y, A1, A2, B1, B2);
    output Y;
    input A1, A2, B1, B2;

    assign Y = ~((A1 & A2) | (B1 & B2));
endmodule
