import numpy

from utils.file_utils import get_lines


def convert_hexa_char_to_bit(hexa_char):
    num_of_bits = 4
    hexa = int(hexa_char, 16)
    return str(bin(hexa)[2:].zfill(num_of_bits))


def convert_hexa_to_bit(hexa_string):
    return ''.join(convert_hexa_char_to_bit(c) for c in hexa_string)


def add_leading_zeros(to_complete, count_trailing_zeros, num_of_bits):
    return '0' * count_trailing_zeros * num_of_bits + to_complete


def test_convert_hexa_to_bit():
    result = convert_hexa_to_bit('D2FE28')
    assert result == '110100101111111000101000'


def test_convert_hexa_to_bit_withleft_pad():
    result = convert_hexa_to_bit('38006F45291200')
    assert result == '00111000000000000110111101000101001010010001001000000000'


def test_convert_hexa_to_bit_with_0():
    result = convert_hexa_to_bit('01')
    assert result == '00000001'


def test_convert_bin_to_int():
    bin_to_int('110')


def bin_to_int(bits):
    return int(hex(int(bits.zfill(4), 2)), 16)


def test_literal():
    input = 'D2FE28'
    packet = Packet(convert_hexa_to_bit(input))
    assert packet.version == 6
    assert packet.typeId == 4
    assert packet.literal == 2021


def test_operator():
    input = 'EE00D40C823060'
    packet = Packet(convert_hexa_to_bit(input))
    assert packet.version == 7
    assert packet.typeId == 3
    assert len(packet.subpackets) == 3


def test_operator_2():
    input = '38006F45291200'
    packet = Packet(convert_hexa_to_bit(input))
    assert packet.version == 1
    assert packet.typeId == 6
    assert len(packet.subpackets) == 2


def test_sample_1():
    input = '8A004A801A8002F478'
    packet = Packet(convert_hexa_to_bit(input))
    assert packet.version_sum() == 16


def test_sample_2():
    input = '620080001611562C8802118E34'
    packet = Packet(convert_hexa_to_bit(input))
    assert packet.version_sum() == 12


def test_sample_3():
    input = 'C0015000016115A2E0802F182340'
    packet = Packet(convert_hexa_to_bit(input))
    assert packet.version_sum() == 23


def test_sample_4():
    input = 'A0016C880162017C3686B18A3D4780'
    packet = Packet(convert_hexa_to_bit(input))
    assert packet.version_sum() == 31


def test_real_input():
    input = get_lines('day16.txt')[0]
    packet = Packet(convert_hexa_to_bit(input))
    assert packet.version_sum() == 1012


def test_compute_sample_1():
    input = 'C200B40A82'
    packet = Packet(convert_hexa_to_bit(input))
    assert packet.compute() == 3


def test_compute_sample_2():
    input = '04005AC33890'
    packet = Packet(convert_hexa_to_bit(input))
    assert packet.compute() == 54


def test_compute_sample_3():
    input = '880086C3E88112'
    packet = Packet(convert_hexa_to_bit(input))
    assert packet.compute() == 7


def test_compute_sample_4():
    input = 'CE00C43D881120'
    packet = Packet(convert_hexa_to_bit(input))
    assert packet.compute() == 9


def test_compute_sample_5():
    input = 'D8005AC2A8F0'
    packet = Packet(convert_hexa_to_bit(input))
    assert packet.compute() == 1


def test_compute_sample_6():
    input = 'F600BC2D8F'
    packet = Packet(convert_hexa_to_bit(input))
    assert packet.compute() == 0


def test_compute_sample_7():
    input = '9C005AC2F8F0'
    packet = Packet(convert_hexa_to_bit(input))
    assert packet.compute() == 0


def test_compute_sample_8():
    input = '9C0141080250320F1802104A08'
    packet = Packet(convert_hexa_to_bit(input))
    assert packet.compute() == 1


def test_compute_real_input():
    input = get_lines('day16.txt')[0]
    packet = Packet(convert_hexa_to_bit(input))
    assert packet.compute() == 2223947372407


LITERAL = 4


class Packet:
    def __init__(self, bits) -> None:
        self.version = bin_to_int(bits[:3])
        self.typeId = bin_to_int(bits[3:6])
        self.subpackets = list()
        index = 6
        if self.typeId == LITERAL:
            next_start = '1'
            literal = ''
            while next_start == '1':
                next_start = bits[index]
                next_int = bits[index + 1:index + 5]
                literal += next_int
                index += 5
            self.literal = int(literal, 2)
        else:
            length_type = bits[index]
            index += 1
            if length_type == '0':
                sub_packet_length_bits = 15
                sub_packet_length = int(bits[index:index + sub_packet_length_bits], 2)
                index += sub_packet_length_bits
                max_index = index + sub_packet_length
                while index < max_index:
                    packet = Packet(bits[index:max_index])
                    self.subpackets.append(packet)
                    index += packet.last_index
            else:
                sub_packet_length_bits = 11
                nb_of_subpackets = int(bits[index:index + sub_packet_length_bits], 2)
                index += sub_packet_length_bits
                for i in range(nb_of_subpackets):
                    next_packet = Packet(bits[index:])
                    self.subpackets.append(next_packet)
                    index += next_packet.last_index
        self.last_index = index

    def version_sum(self):
        result = self.version
        versions = [packet.version_sum() for packet in self.subpackets]
        result += sum(versions)
        return result

    def compute(self):
        if self.typeId == 4:
            return self.literal

        computes = [packet.compute() for packet in self.subpackets]
        if self.typeId == 0:
            return sum(computes)
        elif self.typeId == 1:
            return numpy.prod(computes)
        elif self.typeId == 2:
            return min(computes)
        elif self.typeId == 3:
            return max(computes)
        elif self.typeId == 5:
            return 1 if computes[0] > computes[1] else 0
        elif self.typeId == 6:
            return 1 if computes[0] < computes[1] else 0
        elif self.typeId == 7:
            return 1 if computes[0] == computes[1] else 0
