import { createClient } from
    "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm";

const SUPABASE_URL =
    "https://waasorfiwgbabogspyse.supabase.co";

const SUPABASE_KEY =
    "sb_publishable_qm5NjdspVPj4P7jBfXL58Q_wjBcaINg";

export const supabase = createClient(
    SUPABASE_URL,
    SUPABASE_KEY
);