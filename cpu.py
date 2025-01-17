"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        self.registers = [0] * 8
        self.sp = 0xF4
        self.pc = 0
        self.ram = [0] * 256
        self.running = False
        self.fl = 0b00000000

    def call_stack(self, func):
        branch_table = {
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b10100010: self.MULT,
            0b01100101: self.INC,
            0b01100110: self.DEC,
            0b01000101: self.PUSH,
            0b01000110: self.POP,
            0b10100000: self.ADD,
            0b01010000: self.CALL,
            0b00010001: self.RET,
            0b10100111: self.CMP,
            0b01010100: self.JMP,
            0b01010101: self.JEQ,
            0b01010110: self.JNE,
            0b00000001: self.HLT
        }
        if func in branch_table:
            branch_table[func]()
        else:
            print('invalid function')
            sys.exit(1)

    def load(self, filename):
        """Load a program into memory."""
        file_path = filename
        my_file = open(f"{file_path}", "r")
        address = 0
        for line in my_file:
            if line[0] == "0" or line[0] == "1":
                command = line.split("#", 1)[0]
                self.ram[address] = int(command, 2)
                address += 1
    
    def alu(self, op, operand_a, operand_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[operand_a] += self.registers[operand_b]
            
        elif op == "MULT":
            self.reg[self.ram[operand_a]] *= self.reg[self.ram[operand_b]]

        elif op == "CMP":
            if operand_a == operand_b:
                self.fl = 0b00000001  # E
                print(f"ALU flag: {self.fl}")

            if operand_a > operand_b:
                self.fl = 0b00000100  # G

            else:
                self.fl = 0b00000010  # L
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.registers[i], end='')

        print()
    
    def ram_read(self, index):
        return self.ram[index]

    def ram_write(self, index, value):
        self.ram[index] = value

    def run(self):
        """Run the CPU."""
        self.running = True
        while self.running:
            ir = self.ram[self.pc]
            self.call_stack(ir)
    
    def LDI(self):
        reg_num = self.ram_read(self.pc+1)
        value = self.ram_read(self.pc+2)
        self.registers[reg_num] = value
        self.pc += 3

    def PRN(self):
        reg_num = self.ram[self.pc+1]
        print(self.registers[reg_num])
        self.pc += 2

    def HLT(self):
        self.running = False
        self.pc += 1

    def MULT(self):
        self.alu('MULT', self.pc+1, self.pc+2)
        self.pc += 3

    def DEC(self):
        self.alu('DEC', self.pc+1, None)

    def INC(self):
        self.alu('INC', self.pc+1, None)

    def ADD(self):
        operand_a = self.ram[self.pc + 1]
        operand_b = self.ram[self.pc + 2]
        self.alu("ADD", operand_a, operand_b)
        self.pc += 3

    def PUSH(self):
        # decrement SP
        self.sp -= 1
        # get next value
        reg_num = self.ram[self.pc + 1]
        value = self.registers[reg_num]
        # store it
        self.ram[self.sp] = value
        self.pc += 2

    def POP(self):
        value = self.ram[self.sp]
        # go to next in ram
        self.registers[self.ram[self.pc + 1]] = value
        # increment sp
        self.sp += 1
        self.pc += 2

    def CALL(self):
        print('Call')
        self.sp -= 1
        self.ram[self.sp] = self.pc
        self.pc = self.registers[self.ram[self.pc + 1]]

    def RET(self):
        print('Ret')
        self.pc = self.ram[self.sp]
        self.pc += 2
        self.sp -= 1
    
    def JNE(self):
        # jump to a given register if 'equal flag' is false
        a = self.fl
        if a == 0:
            self.pc = self.registers[self.ram[self.pc + 1]]
        else:
            self.pc += 2

    def JEQ(self):
        # jump to the register addres if 'equal flag' is true
        a = self.fl
        if a == 1:
            self.pc = self.registers[self.ram[self.pc + 1]]
        elif a == 0:
            self.pc += 2

    def JMP(self):
        self.pc = self.registers[self.ram[self.pc + 1]]
        return True

    def CMP(self):
        # compare 
        operand_a = self.registers[self.ram[self.pc + 1]]
        operand_b = self.registers[self.ram[self.pc + 2]]
        if operand_a == operand_b:
            self.fl = 1
        else:
            self.fl = 0
        self.pc += 3

