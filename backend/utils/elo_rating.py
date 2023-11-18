def cal_result(ra, rb, sa):
        ea = 1 / (1 + 10**((rb - ra) / 400))
        eb = 1 / (1 + 10**((ra - rb) / 400))
        k = 32
        return ra+k*(sa-ea), rb+k*((1-sa)-eb)