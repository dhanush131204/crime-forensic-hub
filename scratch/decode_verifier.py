from utils.dna_logic import decode_from_dna

dna_name = "TATATACATAATTAGCTTTTTTAGTACA"
dna_email = "TGAATCTATCCATCATTCGCTGTTTGAGTCCAAGATAGAGTAAATCTGTCGTTCATTCCTTCGAACGCTCAGTCGGTCGT"

try:
    print(f"Decoded Name: {decode_from_dna(dna_name)}")
    print(f"Decoded Email: {decode_from_dna(dna_email)}")
except Exception as e:
    print(f"Decode Error: {e}")
