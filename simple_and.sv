// simple_and.sv
module simple_and(
  input  logic a,
  input  logic b,
  output logic y
);
  assign y = a & b;
endmodule
