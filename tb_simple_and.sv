// tb_simple_and.sv
`timescale 1ns/1ps

module tb_simple_and;
  logic clk = 0;
  always #5 clk = ~clk;

  logic a, b;
  wire  y;
  simple_and dut(.a(a), .b(b), .y(y));

  // Covergroup covering a, b, y and their full cross
  covergroup cg ();
    cp_a: coverpoint a { bins zero = {0}; bins one = {1}; }
    cp_b: coverpoint b { bins zero = {0}; bins one = {1}; }
    cp_y: coverpoint y { bins zero = {0}; bins one = {1}; }
  endgroup

  cg cg_inst = new();

  // Read up to 4 stimulus vectors from Python output
  reg [1:0] stim_vecs [0:3];
  integer   i;
  initial begin
    $readmemb("stimuli.mem", stim_vecs);
    for (i = 0; i < 4; i++) begin
      {a,b} = stim_vecs[i];
      @(posedge clk) cg_inst.sample();
    end
    cg_inst.display();
    $finish;
  end
endmodule
